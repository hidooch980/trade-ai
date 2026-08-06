class CopyTradingEngine:

    def __init__(self):
        self.traders={}
        self.followers={}


    def register_trader(self,trader_id,data):

        self.traders[trader_id]=data

        return {
            "trader":trader_id,
            "status":"REGISTERED"
        }


    def follow(self,user,trader_id,risk_percent=1):

        self.followers[user]={
            "trader":trader_id,
            "risk_percent":risk_percent,
            "status":"ACTIVE"
        }

        return self.followers[user]


    def copy_signal(self,trader_id,trade):

        result=[]

        for user,data in self.followers.items():

            if data["trader"]==trader_id:

                result.append({
                    "user":user,
                    "trade":trade,
                    "risk":data["risk_percent"]
                })

        return result


copy_engine=CopyTradingEngine()
