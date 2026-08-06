class AITradingMarketplace:

    def __init__(self):
        self.products=[]
        self.traders=[]


    def add_product(self,name,category,price):

        item={
            "name":name,
            "category":category,
            "price":price,
            "status":"ACTIVE"
        }

        self.products.append(item)
        return item


    def register_trader(self,name,score):

        trader={
            "name":name,
            "score":score
        }

        self.traders.append(trader)
        return trader


    def leaderboard(self):

        return sorted(
            self.traders,
            key=lambda x:x["score"],
            reverse=True
        )


marketplace=AITradingMarketplace()
