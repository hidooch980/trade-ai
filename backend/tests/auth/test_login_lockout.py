"""
Brute-force protection on /auth/login.

UserService.authenticate() increments user.failed_login_attempts, but the
route raises 401 without committing, so the increment is rolled away and
`locked_until` is never reached. The route's own 423 branch is also
unreachable, because authenticate() reports a locked account as None.
"""

from datetime import datetime, timezone

from sqlalchemy import select

from app.models.user import User
from app.security.auth.brute_force import MAX_FAILED_ATTEMPTS
from app.security.auth.rate_limit import auth_rate_limiter


async def fail_login(client, username, times):
    """Fails `times` logins, stepping around the per-minute rate limiter."""
    for _ in range(times):
        auth_rate_limiter._attempts.clear()
        res = await client.post(
            "/auth/login", json={"username": username, "password": "wrong-password"}
        )
        assert res.status_code in (401, 423), res.text


async def load(db, username):
    return (
        await db.execute(select(User).where(User.username == username))
    ).scalar_one()


async def test_failed_attempts_are_persisted(client, db, account):
    await fail_login(client, account["username"], 1)

    user = await load(db, account["username"])
    assert user.failed_login_attempts == 1


async def test_account_locks_after_the_limit(client, db, account):
    await fail_login(client, account["username"], MAX_FAILED_ATTEMPTS)

    user = await load(db, account["username"])
    assert user.failed_login_attempts >= MAX_FAILED_ATTEMPTS
    assert user.locked_until is not None
    assert user.locked_until > datetime.now(timezone.utc)


async def test_locked_account_reports_423_even_with_the_right_password(
    client, db, account
):
    await fail_login(client, account["username"], MAX_FAILED_ATTEMPTS)
    auth_rate_limiter._attempts.clear()

    res = await client.post(
        "/auth/login",
        json={"username": account["username"], "password": account["password"]},
    )

    assert res.status_code == 423, res.text


async def test_a_good_login_clears_the_counter(client, db, account):
    await fail_login(client, account["username"], MAX_FAILED_ATTEMPTS - 1)
    auth_rate_limiter._attempts.clear()

    res = await client.post(
        "/auth/login",
        json={"username": account["username"], "password": account["password"]},
    )
    assert res.status_code == 200, res.text

    user = await load(db, account["username"])
    assert user.failed_login_attempts == 0
    assert user.locked_until is None


async def test_unknown_username_is_still_rejected(client, account):
    res = await client.post(
        "/auth/login", json={"username": "ghost", "password": "whatever-123"}
    )
    assert res.status_code == 401


async def test_rate_limiter_still_caps_a_burst(client, account):
    """The per-minute limiter is a separate defence and must keep working."""
    codes = []
    for _ in range(7):
        res = await client.post(
            "/auth/login",
            json={"username": account["username"], "password": "wrong-password"},
        )
        codes.append(res.status_code)

    assert 429 in codes, codes
