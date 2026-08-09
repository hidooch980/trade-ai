class GlobalDashboard:

    def __init__(self):
        self.widgets={}


    def update(self,name,data):

        self.widgets[name]=data

        return {
            "widget":name,
            "updated":True
        }


    def overview(self):

        return {
            "system":"TRADE_AI",
            "status":"ONLINE",
            "widgets":self.widgets
        }


    def alerts(self):

        return {
            "alerts":[],
            "status":"CLEAR"
        }


dashboard=GlobalDashboard()
