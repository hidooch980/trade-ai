from datetime import datetime
from app.market_data.models.candle import Candle
from app.market_data.models.tick import Tick
from app.market_data.services.data_service import MarketDataService

service = MarketDataService()

good_candle = Candle(
    symbol="XAUUSD",
    timeframe="H1",
    open=2380,
    high=2390,
    low=2375,
    close=2385,
    volume=1000,
    timestamp=datetime.now()
)

bad_candle = Candle(
    symbol="XAUUSD",
    timeframe="H1",
    open=2380,
    high=2370,
    low=2380,
    close=2385,
    volume=1000,
    timestamp=datetime.now()
)

good_tick = Tick(
    symbol="XAUUSD",
    bid=2380,
    ask=2381,
    spread=1,
    timestamp=datetime.now()
)

print("GOOD CANDLE:", service.process_candle(good_candle))
print("BAD CANDLE:", service.process_candle(bad_candle))
print("GOOD TICK:", service.process_tick(good_tick))
