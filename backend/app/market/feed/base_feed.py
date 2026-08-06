from abc import ABC, abstractmethod


class BasePriceFeed(ABC):

    @abstractmethod
    async def get_price(self, symbol: str):
        pass

    @abstractmethod
    async def get_candles(self, symbol: str, timeframe: str, limit: int):
        pass
