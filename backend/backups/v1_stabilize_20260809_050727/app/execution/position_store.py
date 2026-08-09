import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

STORE_FILE = Path("/opt/trade-ai/backend/positions.json")


class PositionStore:

    def __init__(self):
        self.positions = []
        self.load()

    def load(self):
        if not STORE_FILE.exists():
            self.positions = []
            return

        try:
            data = json.loads(STORE_FILE.read_text())
            self.positions = data if isinstance(data, list) else []
        except Exception:
            self.positions = []

    def save(self):
        STORE_FILE.parent.mkdir(parents=True, exist_ok=True)

        payload = json.dumps(
            self.positions,
            indent=2,
            ensure_ascii=False
        )

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=STORE_FILE.parent,
            prefix=".positions.",
            suffix=".tmp",
            delete=False
        ) as tmp:
            tmp.write(payload)
            tmp.flush()
            os.fsync(tmp.fileno())
            temp_name = tmp.name

        os.replace(temp_name, STORE_FILE)

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
        old_count = len(self.positions)

        self.positions = [
            p for p in self.positions
            if p.get("ticket") != ticket
        ]

        if len(self.positions) != old_count:
            self.save()

position_store = PositionStore()
