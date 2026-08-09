from app.broker.core.adapter import BrokerAdapter
from app.market.bridge.mt5_bridge import mt5_bridge


class MT5Adapter(BrokerAdapter):
    broker_name = "MT5"
    adapter_type = "METATRADER5"

    async def connect(self, credentials=None, config=None):
        result = await mt5_bridge.connect()

        return {
            "status": result.get("status", "CONNECTED"),
            "connected": True,
            "broker": self.broker_name,
            "adapter": self.adapter_type,
            "mode": "SIMULATION",
        }

    async def disconnect(self):
        mt5_bridge.connected = False
        return {
            "status": "DISCONNECTED",
            "broker": self.broker_name,
            "adapter": self.adapter_type,
        }

    async def get_account(self):
        return await mt5_bridge.get_account()

    async def get_positions(self):
        return await mt5_bridge.get_positions()

    async def get_tick(self, symbol):
        return await mt5_bridge.get_tick(symbol)

    async def send_order(self, order):
        result = await mt5_bridge.send_order(order)

        return {
            **result,
            "broker": self.broker_name,
            "adapter": self.adapter_type,
        }

    async def close_position(self, ticket, price=None):
        result = await mt5_bridge.close_position(ticket, price=price)

        return {
            **result,
            "broker": self.broker_name,
            "adapter": self.adapter_type,
        }
