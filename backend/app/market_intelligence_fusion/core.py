class AIMarketIntelligenceFusion:

    def __init__(self):
        self.price_data=[]
        self.news=[]
        self.sentiments=[]
        self.macro=[]
        self.fusion_results=[]


    def add_price_data(self,data):

        self.price_data.append(data)


    def add_news(self,item):

        self.news.append(item)


    def add_sentiment(self,value):

        self.sentiments.append(value)


    def add_macro(self,data):

        self.macro.append(data)


    def fuse(self):

        result={
            "price":len(self.price_data),
            "news":len(self.news),
            "sentiment":len(self.sentiments),
            "macro":len(self.macro),
            "market_state":"ANALYZED"
        }

        self.fusion_results.append(result)

        return result


    def status(self):

        return {
            "price":len(self.price_data),
            "news":len(self.news),
            "sentiment":len(self.sentiments),
            "macro":len(self.macro),
            "fusion":"ONLINE"
        }


market_fusion=AIMarketIntelligenceFusion()
