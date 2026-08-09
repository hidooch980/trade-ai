from abc import ABC, abstractmethod

class BaseMarketDataProvider(ABC):

    @abstractmethod
    async def get_candles(self, symbol: str, timeframe: str, limit: int = 100):
        pass

    @abstractmethod
    async def get_ticks(self, symbol: str, limit: int = 100):
        pass
