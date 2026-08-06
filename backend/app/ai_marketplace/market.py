class AIMarketplace:

    def __init__(self):
        self.products={}
        self.sales=[]


    def publish(self,name,owner,price):

        self.products[name]={
            "owner":owner,
            "price":price,
            "rating":50,
            "status":"ACTIVE"
        }

        return self.products[name]


    def purchase(self,user,product):

        if product not in self.products:
            return None

        self.sales.append({
            "buyer":user,
            "product":product
        })

        return {
            "purchase":"SUCCESS"
        }


    def rate(self,product,score):

        if product in self.products:
            self.products[product]["rating"]=score

        return self.products.get(product)


marketplace=AIMarketplace()
