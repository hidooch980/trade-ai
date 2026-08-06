from datetime import datetime
from .base_feed import BasePriceFeed
from app.market.bridge.mt5_bridge import mt5_bridge


class MT5Feed(BasePriceFeed):

    def __init__(self):
        self.connected = False

    async def connect(self):
        self.connected = True

    async def get_price(self, symbol: str):

        if not self.connected:
            await self.connect()

        return await mt5_bridge.get_tick(symbol)


    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 100
    ):
        return []
