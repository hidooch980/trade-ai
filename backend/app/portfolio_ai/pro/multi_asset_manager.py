class MultiAssetPortfolioAI:

    def __init__(self):
        self.assets={}


    def add_asset(self,symbol,risk,score):

        self.assets[symbol]={
            "risk":risk,
            "score":score
        }

        return self.assets[symbol]


    def allocation(self):

        total_score=sum(
            x["score"]
            for x in self.assets.values()
        )

        result={}

        for symbol,data in self.assets.items():

            if total_score:
                result[symbol]=round(
                    (data["score"]/total_score)*100,
                    2
                )
            else:
                result[symbol]=0

        return result


    def risk_check(self,max_risk=5):

        risk=sum(
            x["risk"]
            for x in self.assets.values()
        )

        return {
            "approved":risk<=max_risk,
            "total_risk":risk
        }


portfolio_ai=MultiAssetPortfolioAI()
