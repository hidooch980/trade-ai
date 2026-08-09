class ProductionBrokerConnector:

    def __init__(self):
        self.connections={}


    def connect(self,name,config):

        self.connections[name]={
            "status":"CONNECTED",
            "config":config
        }

        return self.connections[name]


    def health(self):

        return {
            "brokers":len(self.connections),
            "status":"ONLINE"
        }


    def disconnect(self,name):

        if name in self.connections:
            self.connections[name]["status"]="OFFLINE"

        return self.connections.get(name)


production_broker=ProductionBrokerConnector()
