class AILiveExecutionController:

    def __init__(self):
        self.decisions=[]
        self.orders=[]
        self.events=[]


    def validate_decision(self,data):

        item={
            "decision":data,
            "status":"VALIDATED"
        }

        self.decisions.append(item)

        return item


    def create_order(self,symbol,side,volume):

        order={
            "symbol":symbol,
            "side":side,
            "volume":volume,
            "status":"PENDING"
        }

        self.orders.append(order)

        return order


    def update_event(self,event):

        self.events.append(event)

        return {
            "status":"RECORDED"
        }


    def status(self):

        return {
            "decisions":len(self.decisions),
            "orders":len(self.orders),
            "events":len(self.events),
            "execution":"ONLINE"
        }


live_execution=AILiveExecutionController()
