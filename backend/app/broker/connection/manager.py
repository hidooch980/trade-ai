from __future__ import annotations

from typing import Any

from app.broker.core.router import broker_router
from app.broker.discovery.web_discovery import broker_web_discovery
from app.broker.security.credential_manager import credential_manager
from app.market.bridge.mt5_bridge import mt5_bridge


class BrokerConnectionManager:
    """
    Central broker connection lifecycle.

    Flow:
        broker
        -> discovery
        -> credential resolution
        -> adapter
        -> connection

    Raw credentials are never returned by connection results.

    Connections are keyed by (owner, broker). The engine's own connections
    carry no owner; a user's connection is separate from both the engine's
    and from every other user's.
    """

    def __init__(self):
        self._connections: dict[tuple[str | None, str], Any] = {}

    @staticmethod
    def _normalize(value: str) -> str:
        return str(value or "").strip().lower()

    @staticmethod
    def _owner(owner_id: Any) -> str | None:
        return None if owner_id is None else str(owner_id)

    def _key(self, owner_id: Any, broker_name: str) -> tuple[str | None, str]:
        return (self._owner(owner_id), self._normalize(broker_name))

    async def discover(self, broker_name: str, owner_id: Any = None) -> dict:
        broker_name = str(broker_name or "").strip()

        adapter = broker_router.resolve(broker_name)

        if adapter is not None:
            credential_types = []

            for record in credential_manager.list(owner_id=owner_id):
                if self._normalize(record.broker) == self._normalize(broker_name):
                    credential_types.append(record.connection_type)

            return {
                "success": True,
                "query": broker_name,
                "source": "registered_adapter",
                "profile": {
                    "name": broker_name,
                },
                "adapter": adapter.__name__,
                "ready_for_connection": True,
                "credentials_required": True,
                "credentials_found": bool(credential_types),
                "credential_connection_types": sorted(set(credential_types)),
            }

        return await broker_web_discovery.discover(broker_name)

    async def connect(
        self,
        broker_name: str,
        connection_type: str = "mt5",
        credentials: dict | None = None,
        credential_id: str | None = None,
        config: dict | None = None,
        owner_id: Any = None,
    ) -> dict:
        broker_name = str(broker_name or "").strip()
        connection_type = str(connection_type or "").strip().lower()

        adapter_cls = broker_router.resolve(broker_name)

        if adapter_cls is None:
            discovery = await self.discover(broker_name, owner_id=owner_id)

            return {
                "connected": False,
                "status": "BROKER_NOT_FOUND",
                "broker": broker_name,
                "discovery": discovery,
            }

        # Explicit credentials take precedence.
        if credentials is not None:
            if not isinstance(credentials, dict) or not credentials:
                return {
                    "connected": False,
                    "status": "INVALID_CREDENTIALS",
                    "broker": broker_name,
                    "adapter": adapter_cls.__name__,
                    "connection_type": connection_type,
                }

            stored = credential_manager.store(
                broker=broker_name,
                connection_type=connection_type,
                credentials=credentials,
                owner_id=owner_id,
            )

            credential_id = stored["credential_id"]

        # Resolve existing credential.
        if credential_id is not None:
            try:
                connection_credentials = credential_manager.get(
                    credential_id,
                    owner_id=owner_id,
                )
            except KeyError:
                return {
                    "connected": False,
                    "status": "CREDENTIAL_NOT_FOUND",
                    "broker": broker_name,
                    "adapter": adapter_cls.__name__,
                    "connection_type": connection_type,
                    "credential_id": credential_id,
                }

            metadata = credential_manager.metadata(
                credential_id,
                owner_id=owner_id,
            )

            if (
                self._normalize(metadata["broker"])
                != self._normalize(broker_name)
                or self._normalize(metadata["connection_type"])
                != self._normalize(connection_type)
            ):
                return {
                    "connected": False,
                    "status": "CREDENTIAL_MISMATCH",
                    "broker": broker_name,
                    "adapter": adapter_cls.__name__,
                    "connection_type": connection_type,
                    "credential_id": credential_id,
                }

        else:
            connection_credentials = (
                credential_manager.get_for_connection(
                    broker_name,
                    connection_type,
                    owner_id=owner_id,
                )
            )

        # MT5 simulation bridge does not require real broker credentials.
        # Allow the adapter to establish its simulation connection.
        if connection_credentials is None:
            if (
                self._normalize(broker_name) in {"meta trader 5", "metatrader 5", "metatrader5", "mt5"}
                and connection_type == "mt5"
            ):
                connection_credentials = {}
            else:
                return {
                    "connected": False,
                    "status": "CREDENTIALS_REQUIRED",
                    "broker": broker_name,
                    "adapter": adapter_cls.__name__,
                    "connection_type": connection_type,
                    "credential_id": None,
                }

        adapter = adapter_cls()

        try:
            result = await adapter.connect(
                credentials=connection_credentials,
                # The adapter needs the owner to decide whether it may touch
                # the engine's shared bridge or must isolate itself.
                config={**(config or {}), "owner_id": self._owner(owner_id)},
            )
        except Exception as exc:
            return {
                "connected": False,
                "status": "CONNECTION_ERROR",
                "broker": broker_name,
                "adapter": adapter_cls.__name__,
                "connection_type": connection_type,
                "credential_id": credential_id,
                "error": type(exc).__name__,
            }

        if isinstance(result, dict):
            connected = bool(result.get("connected", True))
            status = result.get("status", "CONNECTED")
        else:
            connected = True
            status = "CONNECTED"

        if not connected:
            return {
                "connected": False,
                "status": status,
                "broker": broker_name,
                "adapter": adapter_cls.__name__,
                "connection_type": connection_type,
                "credential_id": credential_id,
            }

        self._connections[self._key(owner_id, broker_name)] = {
            "adapter": adapter,
            "broker": broker_name,
            "connection_type": connection_type,
            "credential_id": credential_id,
            "owner_id": self._owner(owner_id),
        }

        # Keep the execution bridge synchronized with the broker connection
        # lifecycle. Only the engine's own connection drives the shared
        # bridge — a user connecting their account must not flip it.
        if connection_type == "mt5" and owner_id is None:
            mt5_bridge.connected = True

        return {
            "connected": True,
            "status": status,
            "broker": broker_name,
            "adapter": adapter_cls.__name__,
            "connection_type": connection_type,
            "credential_id": credential_id,
        }

    async def disconnect(self, broker_name: str, owner_id: Any = None) -> dict:
        key = self._key(owner_id, broker_name)

        connection = self._connections.get(key)

        if connection is None:
            return {
                "disconnected": False,
                "status": "NOT_CONNECTED",
                "broker": broker_name,
            }

        adapter = connection["adapter"]

        try:
            result = await adapter.disconnect()
        finally:
            del self._connections[key]

            if connection.get("connection_type") == "mt5" and owner_id is None:
                mt5_bridge.connected = False

        return {
            "disconnected": True,
            "status": (
                result.get("status", "DISCONNECTED")
                if isinstance(result, dict)
                else "DISCONNECTED"
            ),
            "broker": broker_name,
        }

    def connected_brokers(self, owner_id: Any = None) -> list[str]:
        owner = self._owner(owner_id)

        return sorted(
            broker for (record_owner, broker) in self._connections if record_owner == owner
        )

    def is_connected(self, broker_name: str, owner_id: Any = None) -> bool:
        return self._key(owner_id, broker_name) in self._connections

    async def health_check(self, broker_name: str, owner_id: Any = None) -> dict:
        key = self._key(owner_id, broker_name)

        connection = self._connections.get(key)

        if connection is None:
            return {
                "healthy": False,
                "status": "NOT_CONNECTED",
                "broker": broker_name,
            }

        adapter = connection["adapter"]

        try:
            result = await adapter.health_check()

            return {
                "healthy": bool(result.get("healthy", False)),
                "status": result.get("status", "UNKNOWN"),
                "broker": broker_name,
                "adapter": type(adapter).__name__,
            }

        except Exception as exc:
            return {
                "healthy": False,
                "status": "ERROR",
                "broker": broker_name,
                "error": type(exc).__name__,
            }


broker_connection_manager = BrokerConnectionManager()
