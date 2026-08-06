class NeuralTradingBrain:

    def __init__(self):
        self.memory=[]
        self.score=50


    def learn(self,event):

        self.memory.append(event)

        result=event.get("result")

        if result=="WIN":
            self.score=min(
                self.score+5,
                100
            )

        elif result=="LOSS":
            self.score=max(
                self.score-5,
                0
            )

        return {
            "learning_score":self.score,
            "memory_size":len(self.memory)
        }


    def decide(self,signals):

        if not signals:
            return {
                "decision":"WAIT"
            }

        confidence=sum(signals)//len(signals)

        decision="BUY" if confidence>=70 else (
            "SELL" if confidence<=30 else "WAIT"
        )

        return {
            "decision":decision,
            "confidence":confidence
        }


neural_brain=NeuralTradingBrain()
