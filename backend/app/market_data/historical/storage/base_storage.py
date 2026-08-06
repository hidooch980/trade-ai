from abc import ABC, abstractmethod

class BaseMarketStorage(ABC):

    @abstractmethod
    async def save_candles(self, candles):
        pass

    @abstractmethod
    async def load_candles(self, symbol, timeframe, limit=100):
        pass
