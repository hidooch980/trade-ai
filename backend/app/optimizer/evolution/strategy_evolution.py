class StrategyEvolution:
    def __init__(self):
        self.strategies={
            "SMART_MONEY":50,
            "QUANT":50,
            "INDICATORS":50,
            "AI_MODEL":50
        }

    def update(self,results):
        for name,value in results.items():
            if name in self.strategies:
                if value>0:
                    self.strategies[name]=min(self.strategies[name]+5,100)
                else:
                    self.strategies[name]=max(self.strategies[name]-5,0)

        return self.strategies

    def best_strategy(self):
        return max(self.strategies,key=self.strategies.get)

optimizer=StrategyEvolution()
