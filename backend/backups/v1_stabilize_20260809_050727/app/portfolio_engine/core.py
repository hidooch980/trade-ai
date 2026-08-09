class AIPortfolioEngine:

    def __init__(self):
        self.assets=[]
        self.allocations=[]
        self.reports=[]


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


    def create_report(self,data):

        self.reports.append(data)

        return {
            "status":"CREATED"
        }


    def status(self):

        return {
            "assets":len(self.assets),
            "allocations":len(self.allocations),
            "reports":len(self.reports),
            "portfolio":"ONLINE"
        }


portfolio_engine=AIPortfolioEngine()
