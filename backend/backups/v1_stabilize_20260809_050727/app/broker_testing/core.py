class AIBrokerTestingLab:

    def __init__(self):
        self.brokers=[]
        self.accounts=[]
        self.tests=[]
        self.rankings=[]


    def add_broker(self,name):

        broker={
            "name":name,
            "status":"REGISTERED"
        }

        self.brokers.append(broker)

        return broker


    def create_demo_account(self,broker,account):

        item={
            "broker":broker,
            "account":account
        }

        self.accounts.append(item)

        return item


    def run_test(self,broker,result):

        test={
            "broker":broker,
            "result":result
        }

        self.tests.append(test)

        return test


    def rank_broker(self,broker,score):

        ranking={
            "broker":broker,
            "score":score
        }

        self.rankings.append(ranking)

        return ranking


    def status(self):

        return {
            "brokers":len(self.brokers),
            "accounts":len(self.accounts),
            "tests":len(self.tests),
            "rankings":len(self.rankings),
            "broker_lab":"ONLINE"
        }


broker_testing=AIBrokerTestingLab()
