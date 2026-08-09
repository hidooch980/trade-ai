class MarketSentimentAI:

    def __init__(self):
        self.events=[]
        self.sentiments=[]


    def collect_event(self,event):

        self.events.append(event)

        return {
            "status":"COLLECTED"
        }


    def analyze(self,data):

        sentiment={
            "data":data,
            "emotion":"ANALYZED"
        }

        self.sentiments.append(sentiment)

        return sentiment


    def fear_greed(self):

        return {
            "index":"CALCULATED",
            "status":"READY"
        }


    def status(self):

        return {
            "events":len(self.events),
            "sentiments":len(self.sentiments),
            "engine":"ONLINE"
        }


market_sentiment_ai=MarketSentimentAI()
