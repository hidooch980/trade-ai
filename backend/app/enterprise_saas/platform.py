class EnterpriseSaaS:

    def __init__(self):
        self.tenants={}
        self.plans={
            "FREE":0,
            "PRO":99,
            "ENTERPRISE":999
        }


    def create_tenant(self,name,plan="FREE"):

        self.tenants[name]={
            "plan":plan,
            "users":[],
            "status":"ACTIVE"
        }

        return self.tenants[name]


    def add_user(self,tenant,user,role):

        if tenant not in self.tenants:
            return None

        self.tenants[tenant]["users"].append({
            "user":user,
            "role":role
        })

        return True


    def usage(self):

        return {
            "tenants":len(self.tenants),
            "platform":"ONLINE"
        }


enterprise_saas=EnterpriseSaaS()
