from datetime import datetime
from app.market_data.providers.base_provider import BaseMarketDataProvider
from app.market_data.models.candle import Candle
from app.market_data.models.tick import Tick

class MockMarketDataProvider(BaseMarketDataProvider):

    async def get_candles(self, symbol: str, timeframe: str, limit: int = 100):
        return [
            Candle(
                symbol=symbol,
                timeframe=timeframe,
                open=2380,
                high=2390,
                low=2375,
                close=2385,
                volume=1000,
                timestamp=datetime.now()
            )
        ]

    async def get_ticks(self, symbol: str, limit: int = 100):
        return [
            Tick(
                symbol=symbol,
                bid=2380,
                ask=2381,
                spread=1,
                timestamp=datetime.now()
            )
        ]
