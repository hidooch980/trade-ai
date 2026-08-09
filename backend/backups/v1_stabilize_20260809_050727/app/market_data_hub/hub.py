class AIMarketDataHub:

    def __init__(self):
        self.sources={}
        self.streams=[]
        self.history=[]


    def register_source(self,name,source_type):

        self.sources[name]={
            "type":source_type,
            "status":"ACTIVE"
        }

        return self.sources[name]


    def receive_data(self,source,data):

        item={
            "source":source,
            "data":data
        }

        self.streams.append(item)

        return item


    def store_history(self,data):

        self.history.append(data)

        return {
            "status":"STORED"
        }


    def status(self):

        return {
            "sources":len(self.sources),
            "streams":len(self.streams),
            "history":len(self.history),
            "hub":"ONLINE"
        }


market_data_hub=AIMarketDataHub()
