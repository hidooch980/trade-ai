class AIFundManager:

    def __init__(self):
        self.traders={}
        self.capital={}


    def register_trader(self,name):

        self.traders[name]={
            "score":50,
            "capital":0
        }

        return self.traders[name]


    def evaluate(self,name,performance):

        trader=self.traders.get(name)

        if not trader:
            return None

        trader["score"]=performance

        return trader


    def allocate(self,name,amount):

        trader=self.traders.get(name)

        if trader:
            trader["capital"]=amount

        return trader


    def ranking(self):

        return sorted(
            self.traders.items(),
            key=lambda x:x[1]["score"],
            reverse=True
        )


fund_manager=AIFundManager()
