class AIBrokerGateway:

    def __init__(self):
        self.connections=[]
        self.adapters=[]
        self.orders=[]
        self.health=[]


    def connect(self,broker,method):

        connection={
            "broker":broker,
            "method":method,
            "status":"CONNECTED"
        }

        self.connections.append(connection)

        return connection


    def register_adapter(self,name,platform):

        adapter={
            "name":name,
            "platform":platform
        }

        self.adapters.append(adapter)

        return adapter


    def send_order(self,broker,order):

        item={
            "broker":broker,
            "order":order,
            "status":"SENT"
        }

        self.orders.append(item)

        return item


    def check_health(self,broker,status):

        item={
            "broker":broker,
            "status":status
        }

        self.health.append(item)

        return item


    def status(self):

        return {
            "connections":len(self.connections),
            "adapters":len(self.adapters),
            "orders":len(self.orders),
            "health":len(self.health),
            "gateway":"ONLINE"
        }


broker_gateway=AIBrokerGateway()
