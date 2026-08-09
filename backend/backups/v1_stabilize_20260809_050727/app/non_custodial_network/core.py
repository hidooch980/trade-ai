class NonCustodialNetwork:

    def __init__(self):
        self.accounts={}
        self.connections={}


    def connect_broker(self,user,broker,account_id):

        self.connections[user]={
            "broker":broker,
            "account":account_id,
            "status":"CONNECTED"
        }

        return self.connections[user]


    def analyze_account(self,user,data):

        return {
            "user":user,
            "risk":"ANALYZED",
            "data":data
        }


    def request_trade(self,user,order):

        return {
            "user":user,
            "order":order,
            "status":"PENDING_APPROVAL"
        }


    def status(self):

        return {
            "connections":len(self.connections),
            "architecture":"NON_CUSTODIAL"
        }


non_custodial_network=NonCustodialNetwork()
