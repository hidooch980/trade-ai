class StrategyMarketplace:

    def __init__(self):
        self.strategies={}


    def publish(self,owner,name,price):

        strategy={
            "owner":owner,
            "name":name,
            "price":price,
            "rating":50,
            "status":"ACTIVE"
        }

        self.strategies[name]=strategy

        return strategy


    def rate(self,name,result):

        strategy=self.strategies.get(name)

        if not strategy:
            return None

        if result=="GOOD":
            strategy["rating"]=min(
                strategy["rating"]+5,
                100
            )
        else:
            strategy["rating"]=max(
                strategy["rating"]-5,
                0
            )

        return strategy


    def catalog(self):

        return self.strategies


strategy_marketplace=StrategyMarketplace()
