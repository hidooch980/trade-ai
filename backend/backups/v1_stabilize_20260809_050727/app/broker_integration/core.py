class AIBrokerIntegration:

    def __init__(self):
        self.brokers=[]
        self.connections=[]
        self.orders=[]

    def register_broker(self,name):
        self.brokers.append(name)

    def connect(self,broker):
        item={
            "broker":broker,
            "status":"CONNECTED"
        }
        self.connections.append(item)
        return item

    def send_order(self,order):
        self.orders.append(order)
        return {
            "order":order,
            "status":"SENT"
        }

    def status(self):
        return {
            "brokers":len(self.brokers),
            "connections":len(self.connections),
            "orders":len(self.orders),
            "integration":"ONLINE"
        }


broker_integration=AIBrokerIntegration()
