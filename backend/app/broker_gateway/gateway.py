class AIBrokerGateway:

    def __init__(self):
        self.connections={}
        self.orders=[]
        self.accounts={}


    def connect_broker(self,user,broker):

        self.connections[user]={
            "broker":broker,
            "status":"CONNECTED"
        }

        return self.connections[user]


    def get_account(self,user,data):

        self.accounts[user]=data

        return {
            "user":user,
            "account":data
        }


    def send_order(self,user,order):

        item={
            "user":user,
            "order":order,
            "status":"PENDING"
        }

        self.orders.append(item)

        return item


    def status(self):

        return {
            "connections":len(self.connections),
            "accounts":len(self.accounts),
            "orders":len(self.orders),
            "gateway":"ONLINE"
        }


broker_gateway=AIBrokerGateway()
