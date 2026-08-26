"""
The broker credential vault.

get_for_connection() matched only on broker and connection type, so once two
people had registered MT5 credentials the lookup returned whichever record
happened to be stored first — one user connecting with another user's
password.
"""

import pytest

from app.broker.security.credential_manager import CredentialManager

ALICE = "11111111-1111-1111-1111-111111111111"
BOB = "22222222-2222-2222-2222-222222222222"


@pytest.fixture
def vault():
    return CredentialManager()


def test_lookup_is_scoped_to_the_owner(vault):
    vault.store("MT5", "mt5", {"login": "1001", "password": "alice-secret"}, owner_id=ALICE)
    vault.store("MT5", "mt5", {"login": "2002", "password": "bob-secret"}, owner_id=BOB)

    assert vault.get_for_connection("MT5", "mt5", owner_id=BOB)["login"] == "2002"
    assert vault.get_for_connection("MT5", "mt5", owner_id=ALICE)["login"] == "1001"


def test_an_owner_never_sees_another_owners_record(vault):
    vault.store("MT5", "mt5", {"login": "1001", "password": "alice-secret"}, owner_id=ALICE)

    assert vault.get_for_connection("MT5", "mt5", owner_id=BOB) is None


def test_get_by_id_refuses_a_foreign_owner(vault):
    stored = vault.store(
        "MT5", "mt5", {"login": "1001", "password": "alice-secret"}, owner_id=ALICE
    )

    assert vault.get(stored["credential_id"], owner_id=ALICE)["login"] == "1001"

    with pytest.raises(KeyError):
        vault.get(stored["credential_id"], owner_id=BOB)


def test_listing_can_be_filtered_by_owner(vault):
    vault.store("MT5", "mt5", {"login": "1001", "password": "x"}, owner_id=ALICE)
    vault.store("MT5", "mt5", {"login": "2002", "password": "y"}, owner_id=BOB)

    assert [r.credential_id for r in vault.list(owner_id=ALICE)] != [
        r.credential_id for r in vault.list(owner_id=BOB)
    ]
    assert len(vault.list(owner_id=ALICE)) == 1
    assert len(vault.list()) == 2


def test_delete_refuses_a_foreign_owner(vault):
    stored = vault.store("MT5", "mt5", {"login": "1001", "password": "x"}, owner_id=ALICE)

    assert vault.delete(stored["credential_id"], owner_id=BOB)["deleted"] is False
    assert vault.has(stored["credential_id"]) is True

    assert vault.delete(stored["credential_id"], owner_id=ALICE)["deleted"] is True
    assert vault.has(stored["credential_id"]) is False


def test_metadata_never_carries_credential_values(vault):
    stored = vault.store(
        "MT5", "mt5", {"login": "1001", "password": "alice-secret"}, owner_id=ALICE
    )

    meta = vault.metadata(stored["credential_id"], owner_id=ALICE)
    blob = repr(meta)

    assert "alice-secret" not in blob
    assert meta["sensitive_fields"] == ["password"]


def test_unowned_records_stay_reachable_without_an_owner(vault):
    """The engine's own connections do not belong to a user."""
    vault.store("MT5", "mt5", {"login": "9999", "password": "z"})

    assert vault.get_for_connection("MT5", "mt5") is not None
    assert vault.get_for_connection("MT5", "mt5", owner_id=ALICE) is None
