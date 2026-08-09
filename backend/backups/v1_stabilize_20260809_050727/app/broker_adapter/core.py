class BrokerAdapterSystem:

    def __init__(self):
        self.adapters={}
        self.connections=[]
        self.rankings=[]


    def register_adapter(self,name,platform):

        self.adapters[name]={
            "platform":platform,
            "status":"READY"
        }

        return self.adapters[name]


    def test_connection(self,broker):

        result={
            "broker":broker,
            "status":"CONNECTED"
        }

        self.connections.append(result)

        return result


    def add_rating(self,broker,score):

        item={
            "broker":broker,
            "score":score
        }

        self.rankings.append(item)

        return item


    def status(self):

        return {
            "adapters":len(self.adapters),
            "connections":len(self.connections),
            "ratings":len(self.rankings),
            "system":"ONLINE"
        }


broker_adapter=BrokerAdapterSystem()
