class EnterpriseSubscriptionManager:

    def __init__(self):
        self.plans=[]
        self.subscriptions=[]
        self.limits=[]
        self.invoices=[]

    def create_plan(self,data):
        self.plans.append(data)

    def subscribe(self,data):
        self.subscriptions.append(data)

    def set_limit(self,data):
        self.limits.append(data)

    def create_invoice(self,data):
        self.invoices.append(data)

    def status(self):
        return {
            "plans":len(self.plans),
            "subscriptions":len(self.subscriptions),
            "limits":len(self.limits),
            "invoices":len(self.invoices),
            "billing_engine":"ONLINE"
        }


subscription_billing=EnterpriseSubscriptionManager()
