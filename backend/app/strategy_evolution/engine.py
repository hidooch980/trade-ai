class AIStrategyEvolution:

    def __init__(self):
        self.strategies=[]
        self.versions=[]
        self.tests=[]
        self.selected=[]


    def add_strategy(self,name,data):

        strategy={
            "name":name,
            "data":data
        }

        self.strategies.append(strategy)

        return strategy


    def create_version(self,strategy,changes):

        version={
            "strategy":strategy,
            "changes":changes
        }

        self.versions.append(version)

        return version


    def test_strategy(self,version,result):

        test={
            "version":version,
            "result":result
        }

        self.tests.append(test)

        return test


    def select_best(self,version):

        self.selected.append(version)

        return {
            "selected":version,
            "status":"APPROVED"
        }


    def status(self):

        return {
            "strategies":len(self.strategies),
            "versions":len(self.versions),
            "tests":len(self.tests),
            "selected":len(self.selected),
            "evolution":"ONLINE"
        }


strategy_evolution=AIStrategyEvolution()
