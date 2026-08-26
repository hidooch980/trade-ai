"""/api/intelligence — the fused market view."""

from decimal import Decimal


def dec(v) -> Decimal:
    return Decimal(str(v))


async def test_view_requires_authentication(client):
    res = await client.post("/api/intelligence/view", json={"symbol": "EURUSD"})
    assert res.status_code == 401


async def test_meta_lists_the_kinds_and_thresholds(client, member_headers):
    res = await client.get("/api/intelligence/meta", headers=member_headers)
    assert res.status_code == 200, res.text

    body = res.json()
    kinds = {k["kind"] for k in body["kinds"]}
    assert {"TECHNICAL", "SENTIMENT", "MACRO", "NEWS", "LIQUIDITY", "FLOW"} == kinds
    assert dec(body["strong_threshold"]) > dec(body["lean_threshold"])


async def test_agreeing_sources_return_a_buy(client, member_headers):
    res = await client.post(
        "/api/intelligence/view",
        json={
            "symbol": "eurusd",
            "signals": [
                {"kind": "TECHNICAL", "value": "82", "source": "ema-stack"},
                {"kind": "FLOW", "value": "79"},
                {"kind": "MACRO", "value": "77"},
            ],
        },
        headers=member_headers,
    )
    assert res.status_code == 200, res.text

    body = res.json()
    assert body["symbol"] == "EURUSD"
    assert body["decision"] == "BUY"
    assert body["actionable"] is True
    assert dec(body["agreement"]) > 90
    assert body["notes"] == []


async def test_a_split_book_does_not_become_a_trade(client, member_headers):
    res = await client.post(
        "/api/intelligence/view",
        json={
            "symbol": "XAUUSD",
            "signals": [
                {"kind": "TECHNICAL", "value": "95"},
                {"kind": "FLOW", "value": "5"},
                {"kind": "MACRO", "value": "92"},
            ],
        },
        headers=member_headers,
    )

    body = res.json()
    assert "SOURCES_DISAGREE" in body["notes"]
    assert body["decision"] != "BUY"


async def test_a_blocker_stands_aside_without_moving_the_score(
    client, member_headers
):
    payload = {
        "symbol": "EURUSD",
        "signals": [
            {"kind": "TECHNICAL", "value": "85"},
            {"kind": "FLOW", "value": "84"},
        ],
    }

    clean = (
        await client.post("/api/intelligence/view", json=payload, headers=member_headers)
    ).json()
    blocked = (
        await client.post(
            "/api/intelligence/view",
            json={**payload, "blockers": ["NEWS_BLACKOUT"]},
            headers=member_headers,
        )
    ).json()

    assert clean["decision"] == "BUY"
    assert blocked["decision"] == "STAND_ASIDE"
    assert dec(blocked["score"]) == dec(clean["score"])


async def test_contributions_add_up_and_name_the_driver(client, member_headers):
    res = await client.post(
        "/api/intelligence/view",
        json={
            "symbol": "EURUSD",
            "signals": [
                {"kind": "TECHNICAL", "value": "90", "source": "ema-stack"},
                {"kind": "NEWS", "value": "56", "source": "headlines"},
            ],
        },
        headers=member_headers,
    )

    body = res.json()
    total = sum(dec(s["contribution"]) for s in body["sources"])
    assert abs(total - 100) < Decimal("0.01")

    driver = max(body["sources"], key=lambda s: dec(s["contribution"]))
    assert driver["source"] == "ema-stack"


async def test_no_signals_is_a_wait_not_an_error(client, member_headers):
    res = await client.post(
        "/api/intelligence/view", json={"symbol": "EURUSD"}, headers=member_headers
    )

    assert res.status_code == 200
    assert res.json()["decision"] == "WAIT"
    assert "NO_SIGNALS" in res.json()["notes"]


async def test_an_unknown_signal_kind_is_rejected(client, member_headers):
    res = await client.post(
        "/api/intelligence/view",
        json={"symbol": "EURUSD", "signals": [{"kind": "ASTROLOGY", "value": "90"}]},
        headers=member_headers,
    )

    assert res.status_code == 422
