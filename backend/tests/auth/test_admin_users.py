"""/admin/users — listing and moderation, gated on MANAGE_USERS."""

from datetime import datetime, timezone

from sqlalchemy import select

from app.models.auth_session import AuthSession
from app.models.user import User
from app.security.auth.rate_limit import auth_rate_limiter


async def test_listing_requires_authentication(client):
    assert (await client.get("/admin/users")).status_code == 401


async def test_listing_refuses_a_non_admin(client, member_token):
    res = await client.get("/admin/users", headers=member_token)

    assert res.status_code == 403, res.text


async def test_listing_returns_users_with_session_counts(client, admin, account):
    auth_rate_limiter._attempts.clear()
    await client.post(
        "/auth/login",
        json={"username": account["username"], "password": account["password"]},
    )

    res = await client.get("/admin/users", headers=admin["headers"])
    assert res.status_code == 200, res.text

    body = res.json()
    assert body["total"] == 2
    by_name = {item["username"]: item for item in body["items"]}
    assert by_name["trader"]["active_sessions"] == 1
    assert by_name["trader"]["is_locked"] is False
    # A listing must never carry password material.
    assert "password_hash" not in by_name["trader"]


async def test_search_matches_email_and_username(client, admin, account):
    for needle, expected in [("trad", "trader"), ("boss@example", "boss")]:
        res = await client.get(
            "/admin/users", params={"search": needle}, headers=admin["headers"]
        )
        assert res.status_code == 200
        names = [i["username"] for i in res.json()["items"]]
        assert names == [expected], (needle, names)


async def test_pagination_reports_the_full_total(client, admin, account):
    res = await client.get(
        "/admin/users", params={"limit": 1, "offset": 0}, headers=admin["headers"]
    )

    body = res.json()
    assert len(body["items"]) == 1
    assert body["total"] == 2
    assert body["limit"] == 1 and body["offset"] == 0


async def test_role_change(client, db, admin, account):
    res = await client.patch(
        f"/admin/users/{account['id']}/role",
        json={"role": "trader"},
        headers=admin["headers"],
    )
    assert res.status_code == 200, res.text
    assert res.json()["role"] == "TRADER"

    user = (
        await db.execute(select(User).where(User.username == account["username"]))
    ).scalar_one()
    await db.refresh(user)
    assert user.role == "TRADER"


async def test_role_change_rejects_an_unknown_role(client, admin, account):
    res = await client.patch(
        f"/admin/users/{account['id']}/role",
        json={"role": "SUPERUSER"},
        headers=admin["headers"],
    )
    assert res.status_code == 422


async def test_admin_cannot_change_their_own_role(client, admin):
    res = await client.patch(
        f"/admin/users/{admin['id']}/role",
        json={"role": "VIEWER"},
        headers=admin["headers"],
    )
    assert res.status_code == 400


async def test_lock_blocks_login_and_kills_sessions(client, db, admin, account):
    auth_rate_limiter._attempts.clear()
    first = await client.post(
        "/auth/login",
        json={"username": account["username"], "password": account["password"]},
    )
    assert first.status_code == 200

    res = await client.post(
        f"/admin/users/{account['id']}/lock",
        json={"minutes": 30},
        headers=admin["headers"],
    )
    assert res.status_code == 200, res.text
    assert res.json()["is_locked"] is True
    assert res.json()["active_sessions"] == 0

    sessions = (
        await db.execute(
            select(AuthSession).where(AuthSession.user_id == first.json()["user"]["id"])
        )
    ).scalars().all()
    assert sessions and all(s.revoked_at is not None for s in sessions)

    auth_rate_limiter._attempts.clear()
    blocked = await client.post(
        "/auth/login",
        json={"username": account["username"], "password": account["password"]},
    )
    assert blocked.status_code == 423


async def test_unlock_restores_login(client, admin, account):
    await client.post(
        f"/admin/users/{account['id']}/lock", json={}, headers=admin["headers"]
    )

    res = await client.post(
        f"/admin/users/{account['id']}/unlock", headers=admin["headers"]
    )
    assert res.status_code == 200, res.text
    assert res.json()["is_locked"] is False
    assert res.json()["failed_login_attempts"] == 0

    auth_rate_limiter._attempts.clear()
    ok = await client.post(
        "/auth/login",
        json={"username": account["username"], "password": account["password"]},
    )
    assert ok.status_code == 200, ok.text


async def test_admin_cannot_lock_themselves_out(client, admin):
    res = await client.post(
        f"/admin/users/{admin['id']}/lock", json={}, headers=admin["headers"]
    )
    assert res.status_code == 400


async def test_revoke_sessions(client, admin, account):
    auth_rate_limiter._attempts.clear()
    await client.post(
        "/auth/login",
        json={"username": account["username"], "password": account["password"]},
    )

    res = await client.post(
        f"/admin/users/{account['id']}/revoke-sessions", headers=admin["headers"]
    )
    assert res.status_code == 200, res.text
    assert res.json()["active_sessions"] == 0


async def test_locked_filter(client, admin, account):
    await client.post(
        f"/admin/users/{account['id']}/lock", json={}, headers=admin["headers"]
    )

    locked = await client.get(
        "/admin/users", params={"locked": True}, headers=admin["headers"]
    )
    unlocked = await client.get(
        "/admin/users", params={"locked": False}, headers=admin["headers"]
    )

    assert [i["username"] for i in locked.json()["items"]] == ["trader"]
    assert [i["username"] for i in unlocked.json()["items"]] == ["boss"]


async def test_unknown_user_is_404(client, admin):
    res = await client.get(
        "/admin/users/00000000-0000-0000-0000-000000000000",
        headers=admin["headers"],
    )
    assert res.status_code == 404


async def test_admin_can_read_another_users_sessions(client, admin, account):
    auth_rate_limiter._attempts.clear()
    await client.post(
        "/auth/login",
        json={
            "username": account["username"],
            "password": account["password"],
            "device_name": "kitchen-laptop",
        },
    )

    res = await client.get(
        f"/admin/users/{account['id']}/sessions", headers=admin["headers"]
    )
    assert res.status_code == 200, res.text

    rows = res.json()
    assert [r["device_name"] for r in rows] == ["kitchen-laptop"]
    # Session listings must not leak the refresh token hash.
    assert "refresh_token_hash" not in rows[0]
    assert datetime.fromisoformat(rows[0]["expires_at"]) > datetime.now(timezone.utc)
