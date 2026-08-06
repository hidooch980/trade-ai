class MultiTenantManager:

    def __init__(self):
        self.tenants=[]
        self.organizations=[]
        self.isolation_rules=[]
        self.subscriptions=[]

    def create_tenant(self,data):
        self.tenants.append(data)

    def register_organization(self,data):
        self.organizations.append(data)

    def add_isolation_rule(self,data):
        self.isolation_rules.append(data)

    def register_subscription(self,data):
        self.subscriptions.append(data)

    def status(self):
        return {
            "tenants":len(self.tenants),
            "organizations":len(self.organizations),
            "isolation_rules":len(self.isolation_rules),
            "subscriptions":len(self.subscriptions),
            "saas_layer":"ONLINE"
        }


multi_tenant=MultiTenantManager()
