import json
from pathlib import Path

MEMORY=Path("data/self_learning.json")


class SelfLearningAI:

    def __init__(self):
        self.weights={
            "technical":25,
            "quant":20,
            "smart_money":20,
            "risk":15,
            "macro":10,
            "news":10
        }

    def record(self,trade):
        MEMORY.parent.mkdir(exist_ok=True)

        data=[]

        if MEMORY.exists():
            data=json.loads(MEMORY.read_text())

        data.append(trade)

        MEMORY.write_text(
            json.dumps(data,indent=2)
        )

        return {
            "saved":True,
            "total":len(data)
        }


    def learn(self,performance):

        for name,value in performance.items():

            if name in self.weights:

                if value>0:
                    self.weights[name]=min(
                        self.weights[name]+2,40
                    )
                else:
                    self.weights[name]=max(
                        self.weights[name]-2,5
                    )

        return self.weights


self_learning_ai=SelfLearningAI()
