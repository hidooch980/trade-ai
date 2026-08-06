class StrategyFactory:

    def __init__(self):
        self.strategies=[]


    def create(self,name,logic):

        strategy={
            "name":name,
            "logic":logic,
            "score":50,
            "status":"TESTING"
        }

        self.strategies.append(strategy)

        return strategy


    def evaluate(self,name,performance):

        for s in self.strategies:

            if s["name"]==name:

                s["score"]=performance
                s["status"]="ACTIVE" if performance>=70 else "REJECTED"

                return s

        return None


    def best(self):

        if not self.strategies:
            return None

        return max(
            self.strategies,
            key=lambda x:x["score"]
        )


strategy_factory=StrategyFactory()
