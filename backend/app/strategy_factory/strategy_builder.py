class StrategyFactory:

    def __init__(self):
        self.strategies=[]

    def create(self,name,config):
        strategy={
            "name":name,
            "config":config,
            "score":50,
            "status":"TESTING"
        }

        self.strategies.append(strategy)
        return strategy


    def evaluate(self,name,results):

        for strategy in self.strategies:

            if strategy["name"]==name:

                score=0

                if results.get("win_rate",0)>=60:
                    score+=30

                if results.get("profit_factor",0)>=1.5:
                    score+=30

                if results.get("drawdown",100)<=10:
                    score+=40

                strategy["score"]=score
                strategy["status"]="READY"

                return strategy


    def best(self):

        if not self.strategies:
            return None

        return max(
            self.strategies,
            key=lambda x:x["score"]
        )


strategy_factory=StrategyFactory()
