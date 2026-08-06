class PaymentInfrastructure:

    def __init__(self):
        self.transactions=[]
        self.accounts={}


    def create_account(self,user):

        self.accounts[user]={
            "balance":0
        }

        return self.accounts[user]


    def payment(self,user,amount):

        if user not in self.accounts:
            return None

        transaction={
            "user":user,
            "amount":amount,
            "status":"SUCCESS"
        }

        self.transactions.append(transaction)

        self.accounts[user]["balance"]+=amount

        return transaction


    def settlement(self):

        return {
            "transactions":len(self.transactions),
            "status":"COMPLETED"
        }


payment_system=PaymentInfrastructure()
