import json
from pathlib import Path
from pathlib import Path


FILE = Path("app/learning/data/strategy_memory_v2.json")


class AdaptiveStrategyMemory:

    def __init__(self):
        if not FILE.exists():
            FILE.write_text("{}")


    def load(self):
        return json.loads(FILE.read_text())


    def save(self,data):
        FILE.write_text(
            json.dumps(data,indent=2)
        )


    def update(
        self,
        strategy,
        pnl
    ):

        memory = self.load()

        if strategy not in memory:
            memory[strategy] = {
                "trades":0,
                "wins":0,
                "losses":0,
                "score":50
            }


        item = memory[strategy]

        item["trades"] += 1


        if pnl > 0:
            item["wins"] += 1
            item["score"] += 5

        else:
            item["losses"] += 1
            item["score"] -= 5


        item["score"] = max(
            0,
            min(100,item["score"])
        )


        self.save(memory)

        return item


    def get_weight(self,strategy):

        memory=self.load()

        return memory.get(
            strategy,
            {
                "score":50
            }
        )


adaptive_strategy_memory = AdaptiveStrategyMemory()


