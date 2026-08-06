class MarketPredictionAI:

    def predict(self,market_data):

        technical=market_data.get("technical",50)
        sentiment=market_data.get("sentiment",50)
        macro=market_data.get("macro",50)

        score=(technical+sentiment+macro)//3

        if score>=70:
            trend="BULLISH"
        elif score<=30:
            trend="BEARISH"
        else:
            trend="NEUTRAL"

        return {
            "trend":trend,
            "confidence":score,
            "probability":{
                "bullish":score,
                "bearish":100-score
            }
        }


forecast_ai=MarketPredictionAI()
