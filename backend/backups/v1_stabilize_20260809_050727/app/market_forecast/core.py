class AIMarketForecast:

    def __init__(self):
        self.features=[]
        self.predictions=[]
        self.confidence=[]
        self.history=[]

    def add_feature(self,data):
        self.features.append(data)

    def predict(self,market):
        result={
            "market":market,
            "prediction":"ANALYZED"
        }
        self.predictions.append(result)
        return result

    def add_confidence(self,value):
        self.confidence.append(value)

    def store_result(self,result):
        self.history.append(result)

    def status(self):
        return {
            "features":len(self.features),
            "predictions":len(self.predictions),
            "confidence":len(self.confidence),
            "history":len(self.history),
            "forecast":"ONLINE"
        }


market_forecast=AIMarketForecast()
