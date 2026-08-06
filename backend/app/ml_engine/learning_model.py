class MachineLearningEngine:

    def __init__(self):
        self.model_score=50
        self.experience=[]


    def learn(self,result):

        self.experience.append(result)

        if result.get("pnl",0)>0:
            self.model_score=min(
                self.model_score+2,
                100
            )
        else:
            self.model_score=max(
                self.model_score-2,
                0
            )

        return {
            "model_score":self.model_score,
            "samples":len(self.experience)
        }


    def predict(self,data):

        return {
            "prediction":"BUY"
            if self.model_score>=70
            else "WAIT",
            "confidence":self.model_score
        }


ml_engine=MachineLearningEngine()
