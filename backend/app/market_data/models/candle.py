from pydantic import BaseModel
from datetime import datetime

class Candle(BaseModel):
    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0
    timestamp: datetime
