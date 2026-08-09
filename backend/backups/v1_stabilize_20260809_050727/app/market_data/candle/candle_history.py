class CandleHistory:

    def __init__(self, limit=500):
        self.limit = limit
        self.history = {}


    def add(
        self,
        symbol,
        candle
    ):

        if symbol not in self.history:
            self.history[symbol] = []


        self.history[symbol].append(candle)


        if len(self.history[symbol]) > self.limit:
            self.history[symbol] = self.history[symbol][-self.limit:]


        return {
            "symbol": symbol,
            "count": len(self.history[symbol]),
            "latest": candle
        }


    def get(
        self,
        symbol
    ):

        return self.history.get(
            symbol,
            []
        )
