from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import hashlib
import secrets


@dataclass
class CredentialRecord:
    broker: str
    connection_type: str
    credential_id: str
    fields: tuple[str, ...]
    metadata: dict[str, Any] = field(default_factory=dict)


class CredentialManager:
    """Secure in-memory credential manager."""

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

    def store(
        self,
        broker: str,
        connection_type: str,
        credentials: dict[str, Any],
        metadata: dict[str, Any] | None = None,
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
        }

        return {
            "stored": True,
            "credential_id": credential_id,
            "broker": str(broker),
            "connection_type": str(connection_type),
            "fields": sorted(str(k) for k in credentials.keys()),
        }

    def get(self, credential_id: str) -> dict[str, Any]:
        record = self._records.get(str(credential_id))

        if record is None:
            raise KeyError("Credential record not found")

        return dict(record["credentials"])

    def get_for_connection(
        self,
        broker: str,
        connection_type: str,
    ) -> dict[str, Any] | None:
        broker = str(broker)
        connection_type = str(connection_type)

        for record in self._records.values():
            if (
                record["broker"] == broker
                and record["connection_type"] == connection_type
            ):
                return dict(record["credentials"])

        return None

    def metadata(self, credential_id: str) -> dict[str, Any]:
        credential_id = str(credential_id)
        record = self._records.get(credential_id)

        if record is None:
            raise KeyError("Credential record not found")

        credentials = record["credentials"]

        return {
            "credential_id": credential_id,
            "broker": record["broker"],
            "connection_type": record["connection_type"],
            "fields": sorted(str(k) for k in credentials.keys()),
            "credential_count": len(credentials),
            "sensitive_fields": sorted(
                str(k)
                for k in credentials.keys()
                if self._is_sensitive(str(k))
            ),
            "metadata": dict(record["metadata"]),
        }

    def list(self) -> list[CredentialRecord]:
        result: list[CredentialRecord] = []

        for credential_id, record in self._records.items():
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
                    metadata=dict(record["metadata"]),
                )
            )

        return result

    def delete(self, credential_id: str) -> dict[str, Any]:
        credential_id = str(credential_id)
        existed = credential_id in self._records

        if existed:
            del self._records[credential_id]

        return {
            "deleted": existed,
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
