class TraderRankingAI:

    def __init__(self):
        self.traders={}


    def register(self,name,data):

        self.traders[name]=data

        return self.score(data)


    def score(self,data):

        profit=data.get("profit",0)
        win=data.get("win_rate",0)
        drawdown=data.get("drawdown",0)

        score=(profit+win)-(drawdown*2)

        return max(round(score),0)


    def ranking(self):

        result=[]

        for name,data in self.traders.items():

            result.append({
                "name":name,
                "score":self.score(data)
            })

        return sorted(
            result,
            key=lambda x:x["score"],
            reverse=True
        )


ranking_ai=TraderRankingAI()
