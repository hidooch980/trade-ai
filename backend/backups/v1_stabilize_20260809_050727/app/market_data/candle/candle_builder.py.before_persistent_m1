import time
from datetime import datetime
from app.market_data.store.market_store import market_store


class CandleBuilder:

    def __init__(self):
        self.candles = {}

    def update(
        self,
        symbol,
        price,
        volume=0,
        timeframe="M1"
    ):

        now = int(time.time() // 60)
        key = f"{symbol}_{timeframe}_{now}"

        old_keys = [
            k for k in self.candles
            if k.startswith(f"{symbol}_{timeframe}_") and k != key
        ]

        for old in old_keys:
            market_store.add_candle(
                symbol,
                self.candles[old]
            )
            del self.candles[old]

        if key not in self.candles:

            self.candles[key] = {
                "symbol": symbol,
                "timeframe": timeframe,
                "timestamp": datetime.utcnow(),
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": volume
            }

        else:

            candle = self.candles[key]

            candle["high"] = max(
                candle["high"],
                price
            )

            candle["low"] = min(
                candle["low"],
                price
            )

            candle["close"] = price
            candle["volume"] += volume


        return self.candles[key]


candle_builder = CandleBuilder()
