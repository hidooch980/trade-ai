from app.market_data.store.market_store import market_store


class CandleManager:


    def push(
        self,
        symbol,
        open_price,
        high,
        low,
        close,
        volume=0,
        timeframe=None,
        timestamp=None
    ):

        candle = {

            "open":open_price,
            "high":high,
            "low":low,
            "close":close,
            "volume":volume,
            "timeframe":timeframe,
            "timestamp":timestamp

        }


        market_store.add_candle(
            symbol,
            candle
        )


        return candle



candle_manager = CandleManager()
