class StrategyFactoryAI:

    def __init__(self):
        self.strategies={}
        self.tests=[]


    def create_strategy(self,name,rules):

        self.strategies[name]={
            "rules":rules,
            "score":0,
            "status":"CREATED"
        }

        return self.strategies[name]


    def backtest(self,name,data):

        result={
            "strategy":name,
            "data":data,
            "result":"TESTED"
        }

        self.tests.append(result)

        return result


    def optimize(self,name,score):

        if name in self.strategies:
            self.strategies[name]["score"]=score
            self.strategies[name]["status"]="OPTIMIZED"

        return self.strategies.get(name)


    def ranking(self):

        return sorted(
            self.strategies.items(),
            key=lambda x:x[1]["score"],
            reverse=True
        )


    def status(self):

        return {
            "strategies":len(self.strategies),
            "tests":len(self.tests),
            "factory":"ONLINE"
        }


strategy_factory=StrategyFactoryAI()
