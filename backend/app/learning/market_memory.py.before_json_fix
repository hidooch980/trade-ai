import json
import os
from datetime import datetime


class MarketMemory:

    def __init__(self):
        self.file = "app/learning/data/market_memory.json"

        if not os.path.exists(self.file):
            with open(self.file,"w") as f:
                json.dump([],f)


    def save(self, data):

        with open(self.file,"r") as f:
            history = json.load(f)

        history.append({
            "time": datetime.utcnow().isoformat(),
            "data": data
        })

        with open(self.file,"w") as f:
            json.dump(
                history,
                f,
                indent=2
            )

        return True


    def add(self, data):
        return self.save(data)


    def get_history(self):

        with open(self.file,"r") as f:
            return json.load(f)


market_memory = MarketMemory()
