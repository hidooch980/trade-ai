"""/api/accounts — registering and managing MetaTrader accounts."""

from sqlalchemy import select

from app.models.trading_account import TradingAccount
from app.security.auth.rate_limit import auth_rate_limiter

MT5 = {
    "name": "Main demo",
    "server": "ICMarketsSC-Demo",
    "login": "51234567",
    "password": "terminal-password",
    "account_kind": "DEMO",
    "broker": "IC Markets",
}


async def register(client, headers, **overrides):
    return await client.post("/api/accounts", json={**MT5, **overrides}, headers=headers)


async def test_registering_requires_authentication(client):
    assert (await client.post("/api/accounts", json=MT5)).status_code == 401
    assert (await client.get("/api/accounts")).status_code == 401


async def test_register_returns_the_account_without_the_password(
    client, member_headers
):
    res = await register(client, member_headers)

    assert res.status_code == 201, res.text
    body = res.json()

    assert body["server"] == MT5["server"]
    assert body["login"] == MT5["login"]
    assert body["status"] == "PENDING"
    assert body["has_credentials"] is True
    assert body["is_default"] is True, "the first account should become default"

    blob = res.text
    assert MT5["password"] not in blob
    assert "credential_ref" not in body
    assert "password" not in body


async def test_the_password_never_reaches_the_database(client, db, member_headers):
    await register(client, member_headers)

    row = (await db.execute(select(TradingAccount))).scalars().one()
    stored = " ".join(str(v) for v in row.__dict__.values())

    assert MT5["password"] not in stored
    assert row.credential_ref, "a vault handle should have been recorded"


async def test_duplicate_login_on_the_same_server_is_rejected(client, member_headers):
    assert (await register(client, member_headers)).status_code == 201

    duplicate = await register(client, member_headers, name="Second try")
    assert duplicate.status_code == 409


async def test_the_same_login_on_another_server_is_fine(client, member_headers):
    assert (await register(client, member_headers)).status_code == 201

    other = await register(client, member_headers, server="ICMarketsSC-Live")
    assert other.status_code == 201, other.text


async def test_listing_only_returns_your_own_accounts(
    client, member_headers, second_account
):
    await register(client, member_headers)
    await register(client, second_account["headers"], name="Their account")

    mine = await client.get("/api/accounts", headers=member_headers)
    theirs = await client.get("/api/accounts", headers=second_account["headers"])

    assert mine.json()["total"] == 1
    assert theirs.json()["total"] == 1
    assert mine.json()["items"][0]["name"] == "Main demo"
    assert theirs.json()["items"][0]["name"] == "Their account"


async def test_another_users_account_is_not_found(
    client, member_headers, second_account
):
    mine = (await register(client, member_headers)).json()

    for call, args in [
        (client.get, ()),
        (client.post, ()),
    ]:
        pass

    assert (
        await client.get(
            f"/api/accounts/{mine['id']}", headers=second_account["headers"]
        )
    ).status_code == 404
    assert (
        await client.patch(
            f"/api/accounts/{mine['id']}",
            json={"name": "hijacked"},
            headers=second_account["headers"],
        )
    ).status_code == 404
    assert (
        await client.post(
            f"/api/accounts/{mine['id']}/connect", headers=second_account["headers"]
        )
    ).status_code == 404
    assert (
        await client.delete(
            f"/api/accounts/{mine['id']}", headers=second_account["headers"]
        )
    ).status_code == 404


async def test_connect_reports_simulation_mode(client, member_headers):
    account = (await register(client, member_headers)).json()

    res = await client.post(
        f"/api/accounts/{account['id']}/connect", headers=member_headers
    )
    assert res.status_code == 200, res.text

    body = res.json()
    assert body["connected"] is True
    # Nothing here reaches a MetaTrader terminal, and the response says so.
    assert body["mode"] == "SIMULATION"
    assert body["account"]["status"] == "CONNECTED"
    assert body["account"]["last_connected_at"] is not None


async def test_connect_refuses_when_the_vault_has_no_password(
    client, member_headers
):
    from app.broker.security.credential_manager import credential_manager

    account = (await register(client, member_headers)).json()
    credential_manager.clear()  # what a process restart looks like

    res = await client.post(
        f"/api/accounts/{account['id']}/connect", headers=member_headers
    )
    assert res.status_code == 409, res.text

    after = await client.get(f"/api/accounts/{account['id']}", headers=member_headers)
    assert after.json()["has_credentials"] is False
    assert after.json()["last_error"] == "CREDENTIALS_REQUIRED"


async def test_credentials_can_be_resupplied(client, member_headers):
    from app.broker.security.credential_manager import credential_manager

    account = (await register(client, member_headers)).json()
    credential_manager.clear()

    res = await client.put(
        f"/api/accounts/{account['id']}/credentials",
        json={"password": "a-new-terminal-password"},
        headers=member_headers,
    )
    assert res.status_code == 200, res.text
    assert res.json()["has_credentials"] is True

    connect = await client.post(
        f"/api/accounts/{account['id']}/connect", headers=member_headers
    )
    assert connect.status_code == 200, connect.text


async def test_disconnect(client, member_headers):
    account = (await register(client, member_headers)).json()
    await client.post(f"/api/accounts/{account['id']}/connect", headers=member_headers)

    res = await client.post(
        f"/api/accounts/{account['id']}/disconnect", headers=member_headers
    )
    assert res.status_code == 200, res.text
    assert res.json()["connected"] is False
    assert res.json()["account"]["status"] == "DISCONNECTED"


async def test_connecting_a_user_account_does_not_flip_the_engine_bridge(
    client, member_headers
):
    """The shared execution bridge belongs to the engine, not to a customer."""
    from app.market.bridge.mt5_bridge import mt5_bridge

    mt5_bridge.connected = False
    account = (await register(client, member_headers)).json()

    await client.post(f"/api/accounts/{account['id']}/connect", headers=member_headers)

    assert mt5_bridge.connected is False


async def test_default_moves_when_asked(client, member_headers):
    first = (await register(client, member_headers)).json()
    second = (
        await register(client, member_headers, name="Live", server="ICMarketsSC-Live")
    ).json()

    assert first["is_default"] is True
    assert second["is_default"] is False

    res = await client.patch(
        f"/api/accounts/{second['id']}",
        json={"make_default": True},
        headers=member_headers,
    )
    assert res.status_code == 200, res.text

    listing = (await client.get("/api/accounts", headers=member_headers)).json()
    defaults = [a["name"] for a in listing["items"] if a["is_default"]]
    assert defaults == ["Live"], listing


async def test_rename(client, member_headers):
    account = (await register(client, member_headers)).json()

    res = await client.patch(
        f"/api/accounts/{account['id']}",
        json={"name": "Renamed"},
        headers=member_headers,
    )
    assert res.status_code == 200
    assert res.json()["name"] == "Renamed"


async def test_delete_wipes_the_credentials_and_repoints_the_default(
    client, db, member_headers
):
    from app.broker.security.credential_manager import credential_manager

    first = (await register(client, member_headers)).json()
    second = (
        await register(client, member_headers, name="Live", server="ICMarketsSC-Live")
    ).json()

    before = credential_manager.count()

    res = await client.delete(f"/api/accounts/{first['id']}", headers=member_headers)
    assert res.status_code == 204, res.text

    assert credential_manager.count() == before - 1

    rows = (await db.execute(select(TradingAccount))).scalars().all()
    assert [str(r.id) for r in rows] == [second["id"]]
    assert rows[0].is_default is True, "the survivor should inherit default"


async def test_account_cap(client, member_headers):
    from app.api.routes.accounts import MAX_ACCOUNTS_PER_USER

    for i in range(MAX_ACCOUNTS_PER_USER):
        res = await register(
            client, member_headers, name=f"Account {i}", server=f"Server-{i}"
        )
        assert res.status_code == 201, res.text

    over = await register(client, member_headers, name="One too many", server="Server-X")
    assert over.status_code == 409


async def test_registering_needs_every_required_field(client, member_headers):
    res = await client.post(
        "/api/accounts", json={"name": "No server"}, headers=member_headers
    )
    assert res.status_code == 422
