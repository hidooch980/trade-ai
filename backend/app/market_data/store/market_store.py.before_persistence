class MarketStore:

    def __init__(self):
        self.history = {}


    def add_candle(self, symbol, candle):

        if symbol not in self.history:
            self.history[symbol] = []

        self.history[symbol].append(candle)

        # نگه داشتن 1000 کندل آخر
        self.history[symbol] = self.history[symbol][-1000:]


    def get(self, symbol):

        return self.history.get(symbol, [])
        

market_store = MarketStore()
