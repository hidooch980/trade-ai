class RevenueEngine:

    def __init__(self):
        self.transactions=[]
        self.wallets={}


    def create_wallet(self,user):

        self.wallets[user]=0

        return {
            "user":user,
            "balance":0
        }


    def deposit(self,user,amount):

        if user not in self.wallets:
            self.create_wallet(user)

        self.wallets[user]+=amount

        self.transactions.append({
            "user":user,
            "type":"DEPOSIT",
            "amount":amount
        })

        return self.wallets[user]


    def commission(self,amount,percent=10):

        fee=amount*(percent/100)

        return {
            "gross":amount,
            "commission":fee,
            "net":amount-fee
        }


    def report(self):

        return {
            "transactions":len(self.transactions),
            "wallets":len(self.wallets)
        }


revenue_engine=RevenueEngine()
