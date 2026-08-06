class AIPortfolioIntelligence:

    def __init__(self):
        self.assets=[]
        self.allocations=[]
        self.risks=[]
        self.rebalances=[]


    def add_asset(self,name,data):

        asset={
            "name":name,
            "data":data
        }

        self.assets.append(asset)

        return asset


    def allocate(self,asset,percentage):

        item={
            "asset":asset,
            "percentage":percentage
        }

        self.allocations.append(item)

        return item


    def analyze_risk(self,portfolio,result):

        item={
            "portfolio":portfolio,
            "risk":result
        }

        self.risks.append(item)

        return item


    def rebalance(self,action):

        self.rebalances.append(action)

        return {
            "status":"REBALANCED"
        }


    def status(self):

        return {
            "assets":len(self.assets),
            "allocations":len(self.allocations),
            "risks":len(self.risks),
            "rebalances":len(self.rebalances),
            "portfolio":"ONLINE"
        }


portfolio_intelligence=AIPortfolioIntelligence()
