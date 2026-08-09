from datetime import datetime
from app.market_data.candle.candle_builder import candle_builder


class TickFeed:

    def __init__(self):
        self.price = None
        self.prices = {}

    def update(
        self,
        symbol,
        price,
        volume=0
    ):

        self.price = price
        self.prices[symbol] = price

        candle = candle_builder.update(
            symbol,
            price,
            volume,
            "M1"
        )

        return {
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "time": datetime.utcnow(),
            "candle": candle,
            "status": "LIVE"
        }


    def get_price(self):

        return {
            "price": self.price
        }


tick_feed = TickFeed()
