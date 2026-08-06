class AIStrategyEvolution:

    def __init__(self):
        self.strategies=[]
        self.tests=[]
        self.rankings=[]
        self.memory=[]


    def generate(self,strategy):

        self.strategies.append(strategy)

        return {
            "status":"GENERATED"
        }


    def mutate(self,strategy,change):

        item={
            "strategy":strategy,
            "change":change
        }

        self.memory.append(item)

        return item


    def evaluate(self,result):

        self.tests.append(result)

        return {
            "status":"EVALUATED"
        }


    def rank(self,strategy,score):

        self.rankings.append({
            "strategy":strategy,
            "score":score
        })


    def status(self):

        return {
            "strategies":len(self.strategies),
            "tests":len(self.tests),
            "rankings":len(self.rankings),
            "memory":len(self.memory),
            "evolution":"ONLINE"
        }


strategy_evolution=AIStrategyEvolution()
