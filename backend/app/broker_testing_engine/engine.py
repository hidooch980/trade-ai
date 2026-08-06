class BrokerTestingEngine:

    def __init__(self):
        self.tests=[]
        self.scores=[]
        self.reports=[]


    def run_test(self,broker,test_type,result):

        item={
            "broker":broker,
            "test":test_type,
            "result":result
        }

        self.tests.append(item)

        return item


    def calculate_score(self,broker,score):

        item={
            "broker":broker,
            "score":score
        }

        self.scores.append(item)

        return item


    def generate_report(self):

        report={
            "tests":len(self.tests),
            "brokers":len(self.scores),
            "status":"READY"
        }

        self.reports.append(report)

        return report


    def status(self):

        return {
            "tests":len(self.tests),
            "scores":len(self.scores),
            "reports":len(self.reports),
            "engine":"ONLINE"
        }


broker_testing_engine=BrokerTestingEngine()
