from datetime import datetime


class MarketDataEngine:


    def __init__(self):
        self.candles = []


    def add_candle(self, candle):

        candle["time"] = datetime.utcnow().isoformat()

        self.candles.append(candle)

        return candle


    def latest(self):

        if not self.candles:
            return None

        return self.candles[-1]


    def validate(self):

        return {

            "ready":
                len(self.candles) >= 10,

            "candles":
                len(self.candles)

        }
