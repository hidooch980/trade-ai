class FinancialEcosystem:

    def __init__(self):
        self.portfolios={}
        self.users={}


    def create_profile(self,user):

        self.users[user]={
            "risk":"MEDIUM",
            "portfolio":None
        }

        return self.users[user]


    def create_portfolio(self,user,assets):

        if user not in self.users:
            return None

        portfolio={
            "owner":user,
            "assets":assets,
            "status":"ACTIVE"
        }

        self.portfolios[user]=portfolio
        self.users[user]["portfolio"]=portfolio

        return portfolio


    def analyze(self,user):

        return {
            "user":user,
            "recommendation":"OPTIMIZE_ALLOCATION",
            "ai":"ACTIVE"
        }


    def status(self):

        return {
            "users":len(self.users),
            "portfolios":len(self.portfolios),
            "system":"ONLINE"
        }


financial_ecosystem=FinancialEcosystem()
