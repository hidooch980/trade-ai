"""
/auth/refresh.

AuthSessionManager.rotate() always returns a 3-tuple, so the route's
`if not result` guard never fires and an unknown token unpacks to
session=None — an AttributeError, surfacing as 500 instead of 401.
"""

from sqlalchemy import select

from app.models.auth_session import AuthSession


async def login(client, account, device="laptop"):
    res = await client.post(
        "/auth/login",
        json={
            "username": account["username"],
            "password": account["password"],
            "device_name": device,
        },
    )
    assert res.status_code == 200, res.text
    return res.json()


async def test_unknown_refresh_token_is_unauthorised(client, account):
    res = await client.post("/auth/refresh", json={"refresh_token": "x" * 60})

    assert res.status_code == 401, res.text


async def test_refresh_rotates_the_token(client, account):
    tokens = await login(client, account)

    res = await client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert res.status_code == 200, res.text

    rotated = res.json()
    assert rotated["refresh_token"] != tokens["refresh_token"]
    assert rotated["user"]["username"] == account["username"]


async def test_replaying_a_rotated_token_kills_every_session(client, db, account):
    tokens = await login(client, account)

    first = await client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert first.status_code == 200

    replay = await client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert replay.status_code == 401

    sessions = (await db.execute(select(AuthSession))).scalars().all()
    assert sessions, "expected the session rows to still exist"
    assert all(s.revoked_at is not None for s in sessions)


async def test_revoked_session_cannot_refresh(client, account):
    tokens = await login(client, account)

    out = await client.post(
        "/auth/logout", json={"refresh_token": tokens["refresh_token"]}
    )
    assert out.status_code == 200

    res = await client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert res.status_code == 401, res.text
