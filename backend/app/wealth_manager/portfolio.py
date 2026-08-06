class WealthManager:

    def __init__(self):
        self.portfolios={}


    def create(self,user):

        self.portfolios[user]={
            "assets":[],
            "balance":0,
            "risk_score":50
        }

        return self.portfolios[user]


    def add_asset(self,user,symbol,amount):

        if user not in self.portfolios:
            self.create(user)

        self.portfolios[user]["assets"].append({
            "symbol":symbol,
            "amount":amount
        })

        return self.portfolios[user]


    def analyze(self,user):

        portfolio=self.portfolios.get(user)

        if not portfolio:
            return None

        return {
            "user":user,
            "assets":len(portfolio["assets"]),
            "risk_score":portfolio["risk_score"],
            "status":"ACTIVE"
        }


wealth_manager=WealthManager()
