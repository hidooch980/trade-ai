from datetime import datetime
from .base_feed import BasePriceFeed
from app.market.data import MarketCandle
from app.market.stream.price_provider import price_provider


class SimulationFeed(BasePriceFeed):

    async def get_price(self, symbol: str):
        return price_provider.get_price(symbol)


    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 100
    ):

        candles = []

        for i in range(limit):
            candles.append(
                MarketCandle(
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=datetime.utcnow(),
                    open=2375,
                    high=2385,
                    low=2370,
                    close=2380,
                    volume=1000
                )
            )

        return candles
