class AIDemoTestingEngine:

    def __init__(self):
        self.accounts=[]
        self.connections=[]
        self.orders=[]
        self.reports=[]


    def add_account(self,broker,account):

        item={
            "broker":broker,
            "account":account,
            "status":"REGISTERED"
        }

        self.accounts.append(item)

        return item


    def test_connection(self,broker,result):

        item={
            "broker":broker,
            "result":result,
            "status":"TESTED"
        }

        self.connections.append(item)

        return item


    def simulate_order(self,order):

        item={
            "order":order,
            "status":"SIMULATED"
        }

        self.orders.append(item)

        return item


    def create_report(self,data):

        self.reports.append(data)

        return {
            "status":"GENERATED"
        }


    def status(self):

        return {
            "accounts":len(self.accounts),
            "connections":len(self.connections),
            "orders":len(self.orders),
            "reports":len(self.reports),
            "demo_lab":"ONLINE"
        }


demo_testing=AIDemoTestingEngine()
