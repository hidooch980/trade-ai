from pydantic import BaseModel
from datetime import datetime

class Tick(BaseModel):
    symbol: str
    bid: float
    ask: float
    spread: float
    timestamp: datetime
