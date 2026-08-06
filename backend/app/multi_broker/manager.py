class MultiBrokerAI:

    def __init__(self):
        self.brokers={}
        self.connections={}


    def register_broker(self,name,features):

        self.brokers[name]={
            "features":features,
            "score":50
        }

        return self.brokers[name]


    def connect_account(self,user,broker):

        self.connections[user]={
            "broker":broker,
            "status":"CONNECTED"
        }

        return self.connections[user]


    def evaluate(self,broker,score):

        if broker in self.brokers:
            self.brokers[broker]["score"]=score

        return self.brokers.get(broker)


    def best_broker(self):

        if not self.brokers:
            return None

        return max(
            self.brokers,
            key=lambda x:self.brokers[x]["score"]
        )


    def status(self):

        return {
            "brokers":len(self.brokers),
            "connections":len(self.connections),
            "engine":"ONLINE"
        }


multi_broker_ai=MultiBrokerAI()
