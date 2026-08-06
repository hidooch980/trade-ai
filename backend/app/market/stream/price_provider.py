import random
from datetime import datetime


class PriceProvider:

    def __init__(self):
        self.price = 2480.0
        self.mode = "SIMULATION"

    def get_price(self, symbol: str):

        if self.mode == "SIMULATION":
            self.price += random.choice([-2, -1, 1, 2])

        return {
            "symbol": symbol,
            "price": round(self.price, 2),
            "volume": 100,
            "time": datetime.utcnow().isoformat()
        }


price_provider = PriceProvider()

