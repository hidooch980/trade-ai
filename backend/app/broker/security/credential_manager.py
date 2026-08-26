from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import hashlib
import secrets

# Distinguishes "no owner filter" from "records with no owner".
_UNSET = object()


@dataclass
class CredentialRecord:
    broker: str
    connection_type: str
    credential_id: str
    fields: tuple[str, ...]
    owner_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class CredentialManager:
    """
    Secure in-memory credential manager.

    Records are optionally owned. Every lookup takes the owner it is acting
    for and will only match records stored under that same owner — a record
    with no owner belongs to the engine itself and is invisible to users.
    Credential values are never returned by metadata() or list().
    """

    SENSITIVE_FIELDS = {
        "password",
        "pass",
        "secret",
        "api_key",
        "apikey",
        "api_secret",
        "access_token",
        "refresh_token",
        "token",
        "private_key",
        "privatekey",
        "secret_key",
        "account_password",
    }

    def __init__(self):
        self._records: dict[str, dict[str, Any]] = {}

    @staticmethod
    def _normalize(value: str) -> str:
        return str(value or "").strip().lower()

    @classmethod
    def _is_sensitive(cls, key: str) -> bool:
        key = cls._normalize(key)
        return (
            key in cls.SENSITIVE_FIELDS
            or any(
                part in key
                for part in (
                    "password",
                    "secret",
                    "token",
                    "private_key",
                    "privatekey",
                )
            )
        )

    @staticmethod
    def _fingerprint(value: str) -> str:
        return hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def _owner(owner_id: Any) -> str | None:
        return None if owner_id is None else str(owner_id)

    def store(
        self,
        broker: str,
        connection_type: str,
        credentials: dict[str, Any],
        metadata: dict[str, Any] | None = None,
        owner_id: Any = None,
    ) -> dict[str, Any]:
        if not broker:
            raise ValueError("broker is required")

        if not connection_type:
            raise ValueError("connection_type is required")

        if not isinstance(credentials, dict) or not credentials:
            raise ValueError(
                "credentials must be a non-empty dictionary"
            )

        credential_id = secrets.token_urlsafe(24)

        self._records[credential_id] = {
            "broker": str(broker),
            "connection_type": str(connection_type),
            "credentials": dict(credentials),
            "metadata": dict(metadata or {}),
            "owner_id": self._owner(owner_id),
        }

        return {
            "stored": True,
            "credential_id": credential_id,
            "broker": str(broker),
            "connection_type": str(connection_type),
            "owner_id": self._owner(owner_id),
            "fields": sorted(str(k) for k in credentials.keys()),
        }

    def _owned(self, credential_id: str, owner_id: Any) -> dict[str, Any] | None:
        record = self._records.get(str(credential_id))

        if record is None:
            return None

        if record.get("owner_id") != self._owner(owner_id):
            return None

        return record

    def get(self, credential_id: str, owner_id: Any = None) -> dict[str, Any]:
        record = self._owned(credential_id, owner_id)

        if record is None:
            # A wrong owner is reported the same as a missing record, so the
            # caller learns nothing about credentials that are not theirs.
            raise KeyError("Credential record not found")

        return dict(record["credentials"])

    def get_for_connection(
        self,
        broker: str,
        connection_type: str,
        owner_id: Any = None,
    ) -> dict[str, Any] | None:
        broker = str(broker)
        connection_type = str(connection_type)
        owner = self._owner(owner_id)

        for record in self._records.values():
            if (
                record["broker"] == broker
                and record["connection_type"] == connection_type
                and record.get("owner_id") == owner
            ):
                return dict(record["credentials"])

        return None

    def metadata(self, credential_id: str, owner_id: Any = None) -> dict[str, Any]:
        credential_id = str(credential_id)
        record = self._owned(credential_id, owner_id)

        if record is None:
            raise KeyError("Credential record not found")

        credentials = record["credentials"]

        return {
            "credential_id": credential_id,
            "broker": record["broker"],
            "connection_type": record["connection_type"],
            "owner_id": record.get("owner_id"),
            "fields": sorted(str(k) for k in credentials.keys()),
            "credential_count": len(credentials),
            "sensitive_fields": sorted(
                str(k)
                for k in credentials.keys()
                if self._is_sensitive(str(k))
            ),
            "metadata": dict(record["metadata"]),
        }

    def list(self, owner_id: Any = _UNSET) -> list[CredentialRecord]:
        """Every record, or only one owner's when owner_id is given."""
        result: list[CredentialRecord] = []
        wanted = None if owner_id is _UNSET else self._owner(owner_id)

        for credential_id, record in self._records.items():
            if owner_id is not _UNSET and record.get("owner_id") != wanted:
                continue

            result.append(
                CredentialRecord(
                    broker=record["broker"],
                    connection_type=record["connection_type"],
                    credential_id=credential_id,
                    fields=tuple(
                        sorted(
                            str(k)
                            for k in record["credentials"].keys()
                        )
                    ),
                    owner_id=record.get("owner_id"),
                    metadata=dict(record["metadata"]),
                )
            )

        return result

    def delete(self, credential_id: str, owner_id: Any = None) -> dict[str, Any]:
        credential_id = str(credential_id)
        record = self._owned(credential_id, owner_id)

        if record is not None:
            del self._records[credential_id]

        return {
            "deleted": record is not None,
            "credential_id": credential_id,
        }

    def has(self, credential_id: str) -> bool:
        return str(credential_id) in self._records

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records.clear()

    def health_check(self) -> dict[str, Any]:
        return {
            "healthy": True,
            "status": "READY",
            "records": len(self._records),
            "persistent_storage": False,
            "credential_values_exposed": False,
        }


credential_manager = CredentialManager()
