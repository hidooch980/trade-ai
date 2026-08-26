"""
/auth/forgot-password and /auth/reset-password.

These two endpoints reference PasswordResetRepository, generate_reset_token,
hash_reset_token, reset_token_expiry and hash_password without importing any
of them, so they raise NameError before this suite passes.
"""

from sqlalchemy import select

from app.models.auth_session import AuthSession
from app.models.password_reset_token import PasswordResetToken
from app.security.auth.password_reset import hash_reset_token


async def issue_token(client, db, email):
    """Runs the forgot-password flow and digs the raw token back out."""
    res = await client.post("/auth/forgot-password", json={"email": email})
    assert res.status_code == 200, res.text
    rows = (await db.execute(select(PasswordResetToken))).scalars().all()
    return res, rows


async def test_forgot_password_stores_a_token(client, db, account):
    res, rows = await issue_token(client, db, account["email"])

    assert res.json()["success"] is True
    assert len(rows) == 1
    assert rows[0].used_at is None
    # The raw token must never be handed back in the response body.
    assert "token" not in res.json()


async def test_forgot_password_hides_unknown_accounts(client, db, account):
    res = await client.post(
        "/auth/forgot-password", json={"email": "nobody@example.com"}
    )

    assert res.status_code == 200
    assert res.json()["success"] is True
    rows = (await db.execute(select(PasswordResetToken))).scalars().all()
    assert rows == []


async def test_reset_password_changes_the_password(client, db, account, monkeypatch):
    captured = {}

    # The endpoint only ever stores the hash, so intercept generation to learn
    # the raw value a real deployment would have emailed out.
    from app.api.routes import auth as auth_routes

    original = auth_routes.generate_reset_token

    def spy():
        captured["token"] = original()
        return captured["token"]

    monkeypatch.setattr(auth_routes, "generate_reset_token", spy)

    await client.post("/auth/forgot-password", json={"email": account["email"]})
    raw = captured["token"]

    res = await client.post(
        "/auth/reset-password", json={"token": raw, "new_password": "a-brand-new-one"}
    )
    assert res.status_code == 200, res.text

    old = await client.post(
        "/auth/login", json={"username": account["username"], "password": account["password"]}
    )
    assert old.status_code == 401

    new = await client.post(
        "/auth/login", json={"username": account["username"], "password": "a-brand-new-one"}
    )
    assert new.status_code == 200, new.text

    stored = (await db.execute(select(PasswordResetToken))).scalars().one()
    assert stored.used_at is not None
    assert stored.token_hash == hash_reset_token(raw)


async def test_reset_password_revokes_every_session(client, db, account, monkeypatch):
    from app.api.routes import auth as auth_routes

    captured = {}
    original = auth_routes.generate_reset_token
    monkeypatch.setattr(
        auth_routes, "generate_reset_token", lambda: captured.setdefault("t", original())
    )

    # Two live sessions before the reset.
    for device in ("laptop", "phone"):
        res = await client.post(
            "/auth/login",
            json={
                "username": account["username"],
                "password": account["password"],
                "device_name": device,
            },
        )
        assert res.status_code == 200, res.text

    await client.post("/auth/forgot-password", json={"email": account["email"]})
    res = await client.post(
        "/auth/reset-password",
        json={"token": captured["t"], "new_password": "a-brand-new-one"},
    )
    assert res.status_code == 200, res.text

    sessions = (await db.execute(select(AuthSession))).scalars().all()
    assert len(sessions) == 2
    assert all(s.revoked_at is not None for s in sessions)


async def test_reset_password_rejects_an_unknown_token(client, account):
    res = await client.post(
        "/auth/reset-password",
        json={"token": "n" * 80, "new_password": "a-brand-new-one"},
    )
    assert res.status_code == 400


async def test_reset_password_rejects_a_used_token(client, account, monkeypatch):
    from app.api.routes import auth as auth_routes

    captured = {}
    original = auth_routes.generate_reset_token
    monkeypatch.setattr(
        auth_routes, "generate_reset_token", lambda: captured.setdefault("t", original())
    )

    await client.post("/auth/forgot-password", json={"email": account["email"]})
    body = {"token": captured["t"], "new_password": "a-brand-new-one"}

    assert (await client.post("/auth/reset-password", json=body)).status_code == 200
    assert (await client.post("/auth/reset-password", json=body)).status_code == 400
