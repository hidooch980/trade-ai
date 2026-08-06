class AIPaperTrading:

    def __init__(self):
        self.accounts={}
        self.orders=[]
        self.reports=[]


    def create_account(self,user,balance):

        self.accounts[user]={
            "balance":balance,
            "equity":balance,
            "status":"DEMO"
        }

        return self.accounts[user]


    def place_order(self,user,order):

        item={
            "user":user,
            "order":order,
            "mode":"PAPER"
        }

        self.orders.append(item)

        return item


    def generate_report(self,user,result):

        report={
            "user":user,
            "result":result,
            "status":"GENERATED"
        }

        self.reports.append(report)

        return report


    def status(self):

        return {
            "accounts":len(self.accounts),
            "orders":len(self.orders),
            "reports":len(self.reports),
            "simulator":"ONLINE"
        }


paper_trading=AIPaperTrading()
