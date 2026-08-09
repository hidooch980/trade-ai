class EnterpriseDashboard:

    def __init__(self):
        self.metrics={}


    def update(self,key,value):
        self.metrics[key]=value
        return self.metrics


    def summary(self):

        return {
            "system":"TRADE_AI",
            "metrics":self.metrics,
            "status":"ONLINE"
        }


    def kpi(self,accounts,trades):

        return {
            "accounts":accounts,
            "trades":trades,
            "activity":"ACTIVE"
        }


dashboard=EnterpriseDashboard()
