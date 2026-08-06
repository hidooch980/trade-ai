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


    def optimize(self,name,result):

        for strategy in self.strategies:

            if strategy["name"]==name:

                if result.get("profit",0)>0:
                    strategy["score"]=min(
                        strategy["score"]+10,
                        100
                    )
                else:
                    strategy["score"]=max(
                        strategy["score"]-10,
                        0
                    )

                strategy["status"]="READY"

                return strategy

        return None


    def best(self):

        if not self.strategies:
            return None

        return max(
            self.strategies,
            key=lambda x:x["score"]
        )


strategy_factory=StrategyFactory()
