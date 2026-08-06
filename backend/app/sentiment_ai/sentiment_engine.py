class SentimentAI:

    def analyze(self,data):

        score=50

        news=data.get("news",0)
        volume=data.get("volume",0)
        social=data.get("social",0)

        score=(score+news+volume+social)//4

        if score>=70:
            sentiment="BULLISH"

        elif score<=30:
            sentiment="BEARISH"

        else:
            sentiment="NEUTRAL"

        return {
            "score":score,
            "sentiment":sentiment,
            "confidence":abs(score-50)*2
        }


    def decision(self,result):

        if result["sentiment"]=="BULLISH":
            return "BUY"

        if result["sentiment"]=="BEARISH":
            return "SELL"

        return "WAIT"


sentiment_ai=SentimentAI()
