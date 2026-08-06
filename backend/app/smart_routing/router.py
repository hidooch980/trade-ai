class AISmartBrokerRouter:

    def __init__(self):
        self.brokers={}
        self.routes=[]
        self.events=[]


    def register_broker(self,name,score):

        self.brokers[name]={
            "score":score,
            "status":"AVAILABLE"
        }

        return self.brokers[name]


    def select_broker(self,market):

        available=list(self.brokers.keys())

        if available:
            broker=available[0]

            route={
                "market":market,
                "broker":broker,
                "status":"SELECTED"
            }

            self.routes.append(route)

            return route

        return None


    def record_event(self,event):

        self.events.append(event)

        return {
            "status":"RECORDED"
        }


    def status(self):

        return {
            "brokers":len(self.brokers),
            "routes":len(self.routes),
            "events":len(self.events),
            "router":"ONLINE"
        }


smart_router=AISmartBrokerRouter()
