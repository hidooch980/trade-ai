class AIAnalyticsWarehouse:

    def __init__(self):
        self.records=[]


    def store(self,data):

        self.records.append(data)

        return {
            "stored":True,
            "total":len(self.records)
        }


    def performance(self):

        wins=0
        losses=0
        profit=0

        for r in self.records:

            pnl=r.get("pnl",0)
            profit+=pnl

            if pnl>0:
                wins+=1
            else:
                losses+=1

        total=wins+losses

        return {
            "trades":total,
            "wins":wins,
            "losses":losses,
            "win_rate":round((wins/total)*100,2) if total else 0,
            "profit":profit
        }


    def insights(self):

        return {
            "ai_analysis":"GENERATED",
            "records":len(self.records)
        }


warehouse=AIAnalyticsWarehouse()
