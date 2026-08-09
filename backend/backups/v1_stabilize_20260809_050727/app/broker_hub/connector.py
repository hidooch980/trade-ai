class BrokerIntegrationHub:

    def __init__(self):
        self.brokers={}


    def connect(self,name,config):

        self.brokers[name]={
            "config":config,
            "status":"CONNECTED"
        }

        return self.brokers[name]


    def health(self,name):

        broker=self.brokers.get(name)

        if not broker:
            return {
                "status":"NOT_FOUND"
            }

        return {
            "broker":name,
            "status":broker["status"]
        }


    def execute(self,broker,order):

        if broker not in self.brokers:
            return {
                "executed":False,
                "reason":"BROKER_OFFLINE"
            }

        return {
            "executed":True,
            "broker":broker,
            "order":order
        }


broker_hub=BrokerIntegrationHub()
