class CommercialPlatform:

    def __init__(self):
        self.customers={}
        self.subscriptions={}


    def register_customer(self,name):

        self.customers[name]={
            "status":"ACTIVE",
            "plan":"FREE"
        }

        return self.customers[name]


    def upgrade(self,name,plan):

        if name in self.customers:
            self.customers[name]["plan"]=plan

        return self.customers.get(name)


    def dashboard(self):

        return {
            "customers":len(self.customers),
            "subscriptions":len(self.subscriptions),
            "platform":"LIVE"
        }


commercial_platform=CommercialPlatform()
