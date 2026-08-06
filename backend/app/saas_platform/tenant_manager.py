class SaaSPlatform:

    def __init__(self):
        self.tenants={}


    def create_tenant(self,name,plan):

        tenant={
            "name":name,
            "plan":plan,
            "status":"ACTIVE",
            "users":0
        }

        self.tenants[name]=tenant

        return tenant


    def add_user(self,name):

        if name in self.tenants:
            self.tenants[name]["users"]+=1

        return self.tenants.get(name)


    def status(self):

        return {
            "tenants":len(self.tenants),
            "service":"ONLINE"
        }


saas_platform=SaaSPlatform()
