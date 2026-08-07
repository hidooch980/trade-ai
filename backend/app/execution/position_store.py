import json
from pathlib import Path

STORE_FILE = Path("/opt/trade-ai/backend/positions.json")


class PositionStore:

    def __init__(self):
        self.positions = []
        self.load()

    def load(self):
        if STORE_FILE.exists():
            try:
                self.positions = json.loads(STORE_FILE.read_text())
            except:
                self.positions = []

    def save(self):
        STORE_FILE.write_text(json.dumps(self.positions, indent=2))

    def add(self, position):
        for p in self.positions:
            if (
                p.get("ticket") == position.get("ticket")
                and p.get("symbol") == position.get("symbol")
                and p.get("side") == position.get("side")
            ):
                return p

        self.positions.append(position)
        self.save()
        return position

    def get_all(self):
        return self.positions

    def remove(self, ticket):
        self.positions = [
            p for p in self.positions
            if p.get("ticket") != ticket
        ]
        self.save()


position_store = PositionStore()
