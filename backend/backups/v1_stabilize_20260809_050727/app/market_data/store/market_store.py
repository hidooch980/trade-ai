import json
from pathlib import Path


class MarketStore:

    def __init__(self):
        self.history = {}
        self.file = Path("app/market_data/store/market_history.json")
        self.load()

    def load(self):
        if self.file.exists():
            try:
                with open(self.file, "r") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = {}

    def save(self):
        self.file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file, "w") as f:
            json.dump(
                self.history,
                f,
                indent=2,
                default=str
            )

    def add_candle(self, symbol, candle):

        if symbol not in self.history:
            self.history[symbol] = []

        self.history[symbol].append(candle)

        self.history[symbol] = self.history[symbol][-1000:]

        self.save()

    def get(self, symbol):
        return self.history.get(symbol, [])


market_store = MarketStore()
