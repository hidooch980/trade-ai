class WhiteLabelPlatform:

    def __init__(self):
        self.tenants={}


    def create_tenant(self,company,brand):

        self.tenants[company]={
            "brand":brand,
            "status":"ACTIVE",
            "users":0
        }

        return self.tenants[company]


    def add_user(self,company):

        tenant=self.tenants.get(company)

        if tenant:
            tenant["users"]+=1

        return tenant


    def configure(self,company,settings):

        tenant=self.tenants.get(company)

        if tenant:
            tenant["settings"]=settings

        return tenant


    def status(self):

        return {
            "organizations":len(self.tenants),
            "platform":"ACTIVE"
        }


white_label=WhiteLabelPlatform()
