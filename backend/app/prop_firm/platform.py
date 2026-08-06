class PropFirmPlatform:

    def __init__(self):
        self.accounts=[]
        self.challenges=[
            2000,
            5000,
            10000,
            25000,
            50000,
            100000,
            200000
        ]


    def create_challenge(self,user,balance):

        if balance not in self.challenges:
            return {"status":"INVALID_ACCOUNT"}

        account={
            "user":user,
            "size":balance,
            "status":"CHALLENGE",
            "profit_target":10,
            "daily_loss":5,
            "max_drawdown":10
        }

        self.accounts.append(account)

        return account


    def evaluate(self,account):

        return {
            "user":account["user"],
            "status":account["status"],
            "size":account["size"]
        }


prop_firm=PropFirmPlatform()
