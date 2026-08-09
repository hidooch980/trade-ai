from abc import ABC, abstractmethod


class MT5Connector(ABC):
    """
    Standard broker interface used by Trade-AI.

    Concrete broker adapters should implement this contract.
    The trading engine must not depend on broker-specific APIs.
    """

    @abstractmethod
    async def connect(self):
        pass

    async def disconnect(self):
        return {"status": "DISCONNECTED"}

    @abstractmethod
    async def get_account(self):
        pass

    async def get_symbol_info(self, symbol):
        return None

    async def get_symbols(self):
        return []

    async def get_tick(self, symbol):
        return None

    async def get_candles(self, symbol, timeframe, limit=100):
        return []

    @abstractmethod
    async def get_positions(self):
        pass

    async def get_orders(self):
        return []

    @abstractmethod
    async def send_order(self, order):
        pass

    async def modify_order(self, ticket, changes):
        return {
            "modified": False,
            "reason": "NOT_SUPPORTED",
            "ticket": ticket,
        }

    @abstractmethod
    async def close_position(self, ticket, price=None):
        pass

    async def cancel_order(self, ticket):
        return {
            "cancelled": False,
            "reason": "NOT_SUPPORTED",
            "ticket": ticket,
        }

    async def normalize_volume(self, symbol, volume):
        return volume

    async def normalize_price(self, symbol, price):
        return price

    async def health_check(self):
        try:
            result = await self.connect()
            return {
                "healthy": True,
                "status": result.get("status", "CONNECTED")
                if isinstance(result, dict)
                else "CONNECTED",
            }
        except Exception as exc:
            return {
                "healthy": False,
                "status": "ERROR",
                "error": type(exc).__name__,
                "message": str(exc),
            }
