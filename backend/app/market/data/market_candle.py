from dataclasses import dataclass
from datetime import datetime


@dataclass
class MarketCandle:

    symbol: str
    timeframe: str
    timestamp: datetime

    open: float
    high: float
    low: float
    close: float

    volume: float

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "timestamp": self.timestamp.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }
