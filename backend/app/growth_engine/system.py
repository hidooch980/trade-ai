class AIGrowthEngine:

    def __init__(self):
        self.users=[]
        self.markets=[]
        self.partners=[]
        self.metrics=[]


    def add_user_growth(self,data):

        self.users.append(data)

        return {
            "growth":"RECORDED"
        }


    def add_market(self,market):

        self.markets.append(market)

        return {
            "market":market,
            "status":"ADDED"
        }


    def add_partner(self,partner):

        self.partners.append(partner)

        return {
            "partner":partner,
            "status":"REGISTERED"
        }


    def add_metric(self,data):

        self.metrics.append(data)

        return {
            "metric":"SAVED"
        }


    def status(self):

        return {
            "users":len(self.users),
            "markets":len(self.markets),
            "partners":len(self.partners),
            "metrics":len(self.metrics),
            "growth":"ONLINE"
        }


growth_engine=AIGrowthEngine()
