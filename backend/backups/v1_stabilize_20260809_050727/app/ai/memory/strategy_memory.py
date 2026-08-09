import json
from pathlib import Path


class StrategyMemory:

    def __init__(self):
        self.file = Path(
            "data/strategy_memory.json"
        )

        self.file.parent.mkdir(
            exist_ok=True
        )

        if not self.file.exists():
            self.file.write_text("{}")


    def save(
        self,
        symbol,
        timeframe,
        strategy
    ):

        data = json.loads(
            self.file.read_text()
        )

        key = f"{symbol}_{timeframe}"

        data[key] = strategy

        self.file.write_text(
            json.dumps(
                data,
                indent=4
            )
        )

        return data[key]


    def get(
        self,
        symbol,
        timeframe
    ):

        data = json.loads(
            self.file.read_text()
        )

        return data.get(
            f"{symbol}_{timeframe}"
        )


strategy_memory = StrategyMemory()
