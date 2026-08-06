class AIMetaTraderBridge:

    def __init__(self):
        self.connections=[]
        self.market_data=[]
        self.orders=[]
        self.feedback=[]


    def connect_terminal(self,version):

        connection={
            "terminal":version,
            "status":"CONNECTED"
        }

        self.connections.append(connection)

        return connection


    def receive_market_data(self,data):

        self.market_data.append(data)

        return {
            "status":"RECEIVED"
        }


    def send_order(self,order):

        item={
            "order":order,
            "status":"VALIDATING"
        }

        self.orders.append(item)

        return item


    def receive_feedback(self,result):

        self.feedback.append(result)

        return {
            "status":"RECORDED"
        }


    def status(self):

        return {
            "connections":len(self.connections),
            "market_data":len(self.market_data),
            "orders":len(self.orders),
            "feedback":len(self.feedback),
            "bridge":"ONLINE"
        }


metatrader_bridge=AIMetaTraderBridge()
