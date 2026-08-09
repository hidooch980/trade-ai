from app.broker.core.adapter import BrokerAdapter


class SimulatorAdapter(BrokerAdapter):
    broker_name = "SIMULATOR"
    adapter_type = "SIMULATION"

    async def connect(self, credentials=None, config=None):
        return {
            "status": "CONNECTED",
            "broker": self.broker_name,
            "adapter": self.adapter_type,
        }

    async def get_account(self):
        return {
            "balance": 10000.0,
            "equity": 10000.0,
            "margin": 0.0,
            "free_margin": 10000.0,
            "currency": "USD",
        }

    async def get_symbols(self):
        return []

    async def get_positions(self):
        return []

    async def send_order(self, order):
        return {
            "executed": True,
            "status": "FILLED",
            "broker": self.broker_name,
            "order": order,
        }

    async def close_position(self, ticket, price=None):
        return {
            "closed": True,
            "ticket": ticket,
            "price": price,
        }
