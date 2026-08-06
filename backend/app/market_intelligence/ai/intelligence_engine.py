class MarketIntelligence:

    def analyze(self,market):
        data={
            "news_score":50,
            "sentiment_score":50,
            "macro_score":50,
            "technical_score":50
        }

        score=sum(data.values())//len(data)

        decision="BUY" if score>=75 else "WAIT"

        return {
            "market":market,
            "score":score,
            "decision":decision,
            "analysis":data
        }


market_intelligence=MarketIntelligence()
