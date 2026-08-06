class MarketIntelligenceAI:

    def __init__(self):
        self.news=[]
        self.signals=[]


    def analyze_news(self,title,text):

        sentiment="NEUTRAL"

        keywords={
            "positive":[
                "growth",
                "strong",
                "profit"
            ],
            "negative":[
                "crisis",
                "loss",
                "risk"
            ]
        }

        content=(title+" "+text).lower()

        if any(k in content for k in keywords["positive"]):
            sentiment="POSITIVE"

        if any(k in content for k in keywords["negative"]):
            sentiment="NEGATIVE"

        result={
            "title":title,
            "sentiment":sentiment
        }

        self.news.append(result)

        return result


    def impact_score(self):

        return {
            "news_count":len(self.news),
            "impact":"CALCULATED"
        }


market_intelligence=MarketIntelligenceAI()
