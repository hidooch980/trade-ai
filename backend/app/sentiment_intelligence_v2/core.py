class AISentimentIntelligence:

    def __init__(self):
        self.news=[]
        self.sentiments=[]
        self.impacts=[]
        self.history=[]

    def add_news(self,item):
        self.news.append(item)

    def analyze_sentiment(self,data):
        self.sentiments.append(data)
        return data

    def evaluate_impact(self,item):
        self.impacts.append(item)

    def save_history(self,item):
        self.history.append(item)

    def status(self):
        return {
            "news":len(self.news),
            "sentiments":len(self.sentiments),
            "impacts":len(self.impacts),
            "history":len(self.history),
            "sentiment_engine":"ONLINE"
        }


sentiment_intelligence = AISentimentIntelligence()
