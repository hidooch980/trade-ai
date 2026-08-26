"""
The localized error handler.

It used to replace every HTTPException detail with a generic message keyed
only on the status code, so a client could never learn why a request failed
— every 409 read "Request error".
"""

MT5 = {
    "name": "Main demo",
    "server": "ICMarketsSC-Demo",
    "login": "51234567",
    "password": "terminal-password",
    "account_kind": "DEMO",
}


async def test_a_specific_detail_survives(client, member_headers):
    assert (
        await client.post("/api/accounts", json=MT5, headers=member_headers)
    ).status_code == 201

    duplicate = await client.post("/api/accounts", json=MT5, headers=member_headers)

    assert duplicate.status_code == 409
    body = duplicate.json()
    assert body["detail"] == "That login is already registered on this server"
    assert body["error"] == "error.http"
    assert body["status_code"] == 409


async def test_a_bare_raise_still_gets_translated_text(client, member_headers):
    res = await client.get(
        "/api/accounts/00000000-0000-0000-0000-000000000000", headers=member_headers
    )

    assert res.status_code == 404
    body = res.json()
    assert body["error"] == "error.not_found"
    assert body["detail"] == "Account not found"
    assert body["message"], "the generic localized message is still carried"


async def test_unauthenticated_requests_keep_the_generic_message(client):
    res = await client.get("/api/accounts")

    assert res.status_code == 401
    assert res.json()["error"] == "error.unauthorized"


async def test_validation_errors_keep_their_field_list(client, member_headers):
    res = await client.post(
        "/api/accounts", json={"name": "missing everything"}, headers=member_headers
    )

    assert res.status_code == 422
    body = res.json()
    assert body["error"] == "error.validation"
    # A UI can print `detail`; `fields` says exactly what was wrong.
    assert isinstance(body["detail"], str)
    assert set(body["fields"]) >= {"server", "login", "password"}
