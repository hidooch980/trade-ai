import random
from datetime import datetime, timedelta
from app.market_data.store.market_store import market_store


class MarketWarmup:

    def generate(self, symbol, price, count=100):
        candles = []

        current = price

        for i in range(count):
            move = random.choice([-2,-1,0,1,2])

            open_price = current
            close_price = current + move

            candle = {
                "symbol": symbol,
                "timeframe": "M1",
                "timestamp": str(datetime.utcnow() - timedelta(minutes=count-i)),
                "open": open_price,
                "high": max(open_price, close_price) + 1,
                "low": min(open_price, close_price) - 1,
                "close": close_price,
                "volume": random.randint(100,500)
            }

            candles.append(candle)
            current = close_price

        for c in candles:
            market_store.add_candle(symbol,c)

        return len(candles)


market_warmup = MarketWarmup()
