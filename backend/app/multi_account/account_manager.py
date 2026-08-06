class MultiAccountManager:

    def __init__(self):
        self.accounts={}


    def create_account(self,user,balance):

        account={
            "user":user,
            "balance":balance,
            "equity":balance,
            "profit":0,
            "drawdown":0,
            "status":"ACTIVE"
        }

        self.accounts[user]=account
        return account


    def update_profit(self,user,profit):

        if user in self.accounts:
            self.accounts[user]["profit"]+=profit
            self.accounts[user]["equity"]+=profit

        return self.accounts.get(user)


    def ranking(self):

        return sorted(
            self.accounts.values(),
            key=lambda x:x["profit"],
            reverse=True
        )


multi_account_manager=MultiAccountManager()
