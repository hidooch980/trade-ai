class BrokerRouter:

    def __init__(self):
        self.brokers={}


    def register(self,name,spread,latency):

        self.brokers[name]={
            "spread":spread,
            "latency":latency,
            "status":"ONLINE"
        }

        return self.brokers[name]


    def best_broker(self):

        if not self.brokers:
            return None

        return min(
            self.brokers,
            key=lambda x:
            self.brokers[x]["spread"]+
            self.brokers[x]["latency"]
        )


    def status(self):

        return self.brokers


broker_router=BrokerRouter()
