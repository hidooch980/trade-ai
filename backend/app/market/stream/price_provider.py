import random
from datetime import datetime


class PriceProvider:

    def __init__(self):
        self.prices = {
            "EURUSD": 1.1000,
            "GBPUSD": 1.2800,
            "XAUUSD": 2430.0,
            "BTCUSD": 63000.0,
            "ETHUSD": 3000.0
        }

        self.mode = "SIMULATION"


    def get_price(self, symbol: str):

        if symbol not in self.prices:
            self.prices[symbol] = 100.0

        if self.mode == "SIMULATION":

            if symbol in ["EURUSD","GBPUSD"]:
                move = random.choice([-0.0005,-0.0002,0.0002,0.0005])

            elif symbol == "XAUUSD":
                move = random.choice([-2,-1,1,2])

            elif symbol == "BTCUSD":
                move = random.choice([-100,-50,50,100])

            else:
                move = random.choice([-1,1])


            self.prices[symbol] += move


        return {
            "symbol": symbol,
            "price": round(self.prices[symbol], 5),
            "volume": 100,
            "time": datetime.utcnow().isoformat()
        }


price_provider = PriceProvider()
