"""/api/risk — policy, headroom and what-if assessment."""

from decimal import Decimal

MT5 = {
    "name": "Main demo",
    "server": "ICMarketsSC-Demo",
    "login": "51234567",
    "password": "terminal-password",
    "account_kind": "DEMO",
}


async def make_account(client, headers, **overrides):
    res = await client.post("/api/accounts", json={**MT5, **overrides}, headers=headers)
    assert res.status_code == 201, res.text
    account = res.json()

    # Connect once so the account carries the bridge's balance and equity.
    connected = await client.post(
        f"/api/accounts/{account['id']}/connect", headers=headers
    )
    assert connected.status_code == 200, connected.text

    return connected.json()["account"]


def rule(body, name):
    return next(r for r in body["rules"] if r["rule"] == name)


def dec(value) -> Decimal:
    """Compare on value, not on however many trailing zeros JSON carried."""
    return Decimal(str(value))


async def test_policy_is_created_with_defaults_on_first_read(client, member_headers):
    account = await make_account(client, member_headers)

    res = await client.get(
        f"/api/risk/accounts/{account['id']}/policy", headers=member_headers
    )
    assert res.status_code == 200, res.text

    body = res.json()
    assert dec(body["max_daily_loss_percent"]) == 5
    assert body["max_open_positions"] == 5
    assert body["peak_equity"] is not None


async def test_policy_can_be_edited_field_by_field(client, member_headers):
    account = await make_account(client, member_headers)

    res = await client.put(
        f"/api/risk/accounts/{account['id']}/policy",
        json={"max_daily_loss_percent": "3", "max_open_positions": 2},
        headers=member_headers,
    )
    assert res.status_code == 200, res.text

    body = res.json()
    assert dec(body["max_daily_loss_percent"]) == 3
    assert body["max_open_positions"] == 2
    # Untouched fields keep their value.
    assert dec(body["max_total_loss_percent"]) == 10


async def test_policy_rejects_a_nonsensical_limit(client, member_headers):
    account = await make_account(client, member_headers)

    res = await client.put(
        f"/api/risk/accounts/{account['id']}/policy",
        json={"max_daily_loss_percent": "-4"},
        headers=member_headers,
    )
    assert res.status_code == 422


async def test_state_reports_full_headroom_on_a_fresh_account(client, member_headers):
    account = await make_account(client, member_headers)

    res = await client.get(
        f"/api/risk/accounts/{account['id']}/state", headers=member_headers
    )
    assert res.status_code == 200, res.text

    body = res.json()
    assert body["decision"] == "ALLOW"
    assert body["allowed"] is True
    assert body["open_positions"] == 0
    assert dec(rule(body, "DAILY_LOSS")["used"]) == 0
    assert dec(rule(body, "DAILY_LOSS")["headroom"]) == 5


async def test_a_sound_trade_is_allowed(client, member_headers):
    account = await make_account(client, member_headers)

    res = await client.post(
        f"/api/risk/accounts/{account['id']}/assess",
        json={
            "trade": {
                "symbol": "EURUSD",
                "side": "BUY",
                "volume": "0.1",
                "entry_price": "1.1000",
                "stop_loss": "1.0980",
            }
        },
        headers=member_headers,
    )
    assert res.status_code == 200, res.text

    body = res.json()
    assert body["decision"] == "ALLOW"
    assert dec(rule(body, "TRADE_RISK")["used"]) == Decimal("0.2")


async def test_a_trade_without_a_stop_is_blocked(client, member_headers):
    account = await make_account(client, member_headers)

    res = await client.post(
        f"/api/risk/accounts/{account['id']}/assess",
        json={
            "trade": {
                "symbol": "EURUSD",
                "side": "BUY",
                "volume": "0.1",
                "entry_price": "1.1000",
            }
        },
        headers=member_headers,
    )

    body = res.json()
    assert body["decision"] == "BLOCK"
    assert body["allowed"] is False
    assert "TRADE_RISK" in body["reasons"]


async def test_a_drawn_down_account_blocks(client, member_headers):
    account = await make_account(client, member_headers)

    # The bridge reports 10,000; ask what 9,400 looks like.
    res = await client.post(
        f"/api/risk/accounts/{account['id']}/assess",
        json={"equity": "9400"},
        headers=member_headers,
    )

    body = res.json()
    assert body["decision"] == "BLOCK"
    assert "DAILY_LOSS" in body["reasons"]
    assert dec(rule(body, "DAILY_LOSS")["used"]) == 6


async def test_supplied_positions_drive_exposure(client, member_headers):
    account = await make_account(client, member_headers)

    res = await client.post(
        f"/api/risk/accounts/{account['id']}/assess",
        json={
            "positions": [
                {
                    "symbol": "EURUSD",
                    "side": "BUY",
                    "volume": "1.5",
                    "entry_price": "1.10",
                }
            ]
        },
        headers=member_headers,
    )

    body = res.json()
    assert body["open_positions"] == 1
    assert dec(body["exposure"]) == 165000
    assert rule(body, "TOTAL_EXPOSURE")["status"] == "BREACH"
    assert body["decision"] == "BLOCK"


async def test_a_tighter_policy_changes_the_verdict(client, member_headers):
    account = await make_account(client, member_headers)

    trade = {
        "trade": {
            "symbol": "EURUSD",
            "side": "BUY",
            "volume": "0.1",
            "entry_price": "1.1000",
            "stop_loss": "1.0980",
        }
    }

    first = await client.post(
        f"/api/risk/accounts/{account['id']}/assess", json=trade, headers=member_headers
    )
    assert first.json()["decision"] == "ALLOW"

    await client.put(
        f"/api/risk/accounts/{account['id']}/policy",
        json={"max_risk_per_trade_percent": "0.1"},
        headers=member_headers,
    )

    second = await client.post(
        f"/api/risk/accounts/{account['id']}/assess", json=trade, headers=member_headers
    )
    assert second.json()["decision"] == "BLOCK"


async def test_the_peak_is_remembered_across_calls(client, member_headers):
    account = await make_account(client, member_headers)

    # A good run lifts the high water mark…
    await client.post(
        f"/api/risk/accounts/{account['id']}/assess",
        json={"equity": "12000"},
        headers=member_headers,
    )

    # …so giving it all back is measured from 12,000, not from 10,000.
    res = await client.post(
        f"/api/risk/accounts/{account['id']}/assess",
        json={"equity": "10000"},
        headers=member_headers,
    )

    body = res.json()
    assert dec(body["peak_equity"]) == 12000
    assert Decimal("16.6") < dec(rule(body, "TOTAL_LOSS")["used"]) < Decimal("16.7")
    assert body["decision"] == "BLOCK"


async def test_day_reset_moves_the_daily_reference(client, member_headers):
    account = await make_account(client, member_headers)

    res = await client.post(
        f"/api/risk/accounts/{account['id']}/day-reset", headers=member_headers
    )
    assert res.status_code == 200, res.text
    assert res.json()["day_start_equity"] is not None
    assert res.json()["day_started_at"] is not None


async def test_risk_routes_are_scoped_to_the_owner(
    client, member_headers, second_account
):
    account = await make_account(client, member_headers)
    theirs = second_account["headers"]

    assert (
        await client.get(f"/api/risk/accounts/{account['id']}/policy", headers=theirs)
    ).status_code == 404
    assert (
        await client.get(f"/api/risk/accounts/{account['id']}/state", headers=theirs)
    ).status_code == 404
    assert (
        await client.post(
            f"/api/risk/accounts/{account['id']}/assess", json={}, headers=theirs
        )
    ).status_code == 404
    assert (
        await client.put(
            f"/api/risk/accounts/{account['id']}/policy",
            json={"max_open_positions": 99},
            headers=theirs,
        )
    ).status_code == 404


async def test_risk_routes_require_authentication(client):
    fake = "00000000-0000-0000-0000-000000000000"
    assert (await client.get(f"/api/risk/accounts/{fake}/state")).status_code == 401


async def test_state_and_policy_can_be_asked_for_at_once(client, member_headers):
    """
    The dashboard fires both on mount. Both create the policy row if it is
    missing, and the loser of that race must read the winner's row rather
    than fail on the unique constraint.
    """
    import asyncio

    account = await make_account(client, member_headers)

    state, policy = await asyncio.gather(
        client.get(f"/api/risk/accounts/{account['id']}/state", headers=member_headers),
        client.get(f"/api/risk/accounts/{account['id']}/policy", headers=member_headers),
    )

    assert state.status_code == 200, state.text
    assert policy.status_code == 200, policy.text
    assert policy.json()["account_id"] == account["id"]
