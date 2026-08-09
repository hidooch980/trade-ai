class AccountFactory:

    def __init__(self):
        self.accounts={}


    def create(self,account_id,size,challenge):

        self.accounts[account_id]={
            "size":size,
            "challenge":challenge,
            "status":"ACTIVE",
            "profit":0,
            "drawdown":0
        }

        return self.accounts[account_id]


    def update(self,account_id,profit,drawdown):

        if account_id in self.accounts:
            self.accounts[account_id]["profit"]=profit
            self.accounts[account_id]["drawdown"]=drawdown

        return self.accounts.get(account_id)


    def list_accounts(self):

        return self.accounts


account_factory=AccountFactory()
