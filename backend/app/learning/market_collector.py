import json
from pathlib import Path
from datetime import datetime


DATA_FILE = Path("/opt/trade-ai/backend/app/learning/data/market_data.json")


class MarketCollector:

    def __init__(self):
        self.data = []
        self.load()

    def load(self):
        if DATA_FILE.exists():
            try:
                self.data = json.loads(DATA_FILE.read_text())
            except:
                self.data = []

    def save(self):
        DATA_FILE.write_text(
            json.dumps(self.data, indent=2)
        )

    def collect(self, market, symbol, payload):
        record = {
            "time": datetime.utcnow().isoformat(),
            "market": market,
            "symbol": symbol,
            "data": payload
        }

        self.data.append(record)
        self.save()

        return record

    def latest(self, count=100):
        return self.data[-count:]

    def size(self):
        return len(self.data)


market_collector = MarketCollector()
