class MarketPredictionEngine:

    def __init__(self):
        self.history=[]


    def predict(self,symbol,data):

        score=50

        if data.get("volume",0)>0:
            score+=10

        if data.get("trend")=="UP":
            score+=20

        if data.get("trend")=="DOWN":
            score-=20

        probability=max(
            min(score,100),
            0
        )

        direction="BUY" if probability>=60 else "WAIT"

        result={
            "symbol":symbol,
            "probability":probability,
            "direction":direction,
            "confidence":probability
        }

        self.history.append(result)

        return result


    def report(self):

        return {
            "predictions":len(self.history),
            "engine":"ACTIVE"
        }


prediction_engine=MarketPredictionEngine()
