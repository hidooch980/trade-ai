from app.ai.memory.adaptive_strategy_memory import adaptive_strategy_memory

import json
import os
from datetime import datetime


class RewardEngine:

    def __init__(self):
        self.file = "app/learning/data/reward_memory.json"

        os.makedirs(
            os.path.dirname(self.file),
            exist_ok=True
        )

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump([], f, indent=2)


    def add_result(self, decision, profit):

        reward = 0

        if profit > 0:
            reward = 1
        elif profit < 0:
            reward = -1

        data = {
            "time": datetime.utcnow().isoformat(),
            "decision": decision,
            "profit": profit,
            "reward": reward
        }

        with open(self.file, "r") as f:
            history = json.load(f)

        history.append(data)

        with open(self.file, "w") as f:
            json.dump(history, f, indent=2)

        return data


    def get_score(self, decision):

        try:
            with open(self.file, "r") as f:
                history = json.load(f)

        except:
            return 0

        score = 0

        for item in history:

            if item["decision"] == decision:
                score += item["reward"]

        return score


reward_engine = RewardEngine()


    
def update_adaptive_learning(decision, profit):
    strategy = "SMART_MONEY_M1"

    return adaptive_strategy_memory.update(
        strategy,
        profit
    )
