from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradeRecord:

    symbol: str
    side: str
    entry: float
    exit: float
    volume: float
    profit: float
    timestamp: datetime


    def to_dict(self):

        return {
            "symbol": self.symbol,
            "side": self.side,
            "entry": self.entry,
            "exit": self.exit,
            "volume": self.volume,
            "profit": self.profit,
            "timestamp": self.timestamp.isoformat()
        }
