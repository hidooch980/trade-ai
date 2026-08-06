class AIExchange:

    def __init__(self):
        self.orders=[]
        self.trades=[]


    def submit_order(self,user,side,asset,amount):

        order={
            "user":user,
            "side":side,
            "asset":asset,
            "amount":amount,
            "status":"OPEN"
        }

        self.orders.append(order)

        return order


    def match_orders(self):

        return {
            "matched":"AI_PROCESSED",
            "orders":len(self.orders)
        }


    def execute(self,order):

        trade={
            "order":order,
            "status":"EXECUTED"
        }

        self.trades.append(trade)

        return trade


    def status(self):

        return {
            "orders":len(self.orders),
            "trades":len(self.trades),
            "exchange":"ONLINE"
        }


ai_exchange=AIExchange()
