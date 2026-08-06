class BrokerCertification:

    def __init__(self):
        self.brokers={}


    def register(self,name):

        self.brokers[name]={
            "status":"TESTING",
            "score":0
        }

        return self.brokers[name]


    def test(self,name,latency,execution):

        broker=self.brokers.get(name)

        if not broker:
            return None

        score=max(
            0,
            100-(latency/10)+execution
        )

        broker["score"]=round(score,2)
        broker["status"]="CERTIFIED"

        return broker


    def ranking(self):

        return sorted(
            self.brokers.items(),
            key=lambda x:x[1]["score"],
            reverse=True
        )


broker_certification=BrokerCertification()
