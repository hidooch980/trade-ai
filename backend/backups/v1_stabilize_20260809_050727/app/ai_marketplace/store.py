class AITradingMarketplace:

    def __init__(self):
        self.products={}
        self.developers={}
        self.orders=[]


    def register_developer(self,name):

        self.developers[name]={
            "status":"ACTIVE"
        }

        return self.developers[name]


    def publish_product(self,name,category,owner):

        self.products[name]={
            "category":category,
            "owner":owner,
            "status":"PUBLISHED"
        }

        return self.products[name]


    def purchase(self,user,product):

        order={
            "user":user,
            "product":product,
            "status":"COMPLETED"
        }

        self.orders.append(order)

        return order


    def status(self):

        return {
            "products":len(self.products),
            "developers":len(self.developers),
            "orders":len(self.orders),
            "marketplace":"ONLINE"
        }


ai_marketplace=AITradingMarketplace()
