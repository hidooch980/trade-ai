from app.broker.core.adapter import BrokerAdapter
from app.market.bridge.mt5_bridge import MT5Bridge, mt5_bridge


class MT5Adapter(BrokerAdapter):
    broker_name = "MT5"
    adapter_type = "METATRADER5"

    def __init__(self):
        # A connection made on behalf of a user gets its own bridge instance.
        # The module-level `mt5_bridge` is the engine's, and its `connected`
        # flag is the hard gate on order submission — a customer connecting
        # their own account must never open it.
        self._bridge: MT5Bridge | None = None

    @property
    def bridge(self) -> MT5Bridge:
        return self._bridge if self._bridge is not None else mt5_bridge

    async def connect(self, credentials=None, config=None):
        owner_id = (config or {}).get("owner_id")

        if owner_id is not None:
            self._bridge = MT5Bridge()

        result = await self.bridge.connect()

        return {
            "status": result.get("status", "CONNECTED"),
            "connected": True,
            "broker": self.broker_name,
            "adapter": self.adapter_type,
            "mode": "SIMULATION",
            "isolated": self._bridge is not None,
        }

    async def disconnect(self):
        self.bridge.connected = False
        return {
            "status": "DISCONNECTED",
            "broker": self.broker_name,
            "adapter": self.adapter_type,
        }

    async def get_account(self):
        return await self.bridge.get_account()

    async def get_positions(self):
        return await self.bridge.get_positions()

    async def get_tick(self, symbol):
        return await self.bridge.get_tick(symbol)

    async def send_order(self, order):
        result = await self.bridge.send_order(order)

        return {
            **result,
            "broker": self.broker_name,
            "adapter": self.adapter_type,
        }

    async def close_position(self, ticket, price=None):
        result = await self.bridge.close_position(ticket, price=price)

        return {
            **result,
            "broker": self.broker_name,
            "adapter": self.adapter_type,
        }
