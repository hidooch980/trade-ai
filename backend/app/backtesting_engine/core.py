class AIBacktestingEngine:

    def __init__(self):
        self.strategies=[]
        self.tests=[]
        self.reports=[]


    def add_strategy(self,name):

        strategy={
            "name":name,
            "status":"READY"
        }

        self.strategies.append(strategy)

        return strategy


    def run_test(self,strategy,data):

        result={
            "strategy":strategy,
            "data":data,
            "status":"COMPLETED"
        }

        self.tests.append(result)

        return result


    def create_report(self,result):

        report={
            "result":result,
            "status":"GENERATED"
        }

        self.reports.append(report)

        return report


    def status(self):

        return {
            "strategies":len(self.strategies),
            "tests":len(self.tests),
            "reports":len(self.reports),
            "engine":"ONLINE"
        }


backtesting_engine=AIBacktestingEngine()
