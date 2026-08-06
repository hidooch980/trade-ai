class AutonomousTradingCore:

    def decide(self,analysis):

        scores=[]

        for engine,result in analysis.items():

            if isinstance(result,dict):
                scores.append(
                    result.get("score",50)
                )

        if not scores:
            return {
                "decision":"WAIT",
                "score":0
            }

        final_score=sum(scores)//len(scores)

        if final_score>=75:
            decision="BUY"

        elif final_score<=25:
            decision="SELL"

        else:
            decision="WAIT"

        return {
            "decision":decision,
            "score":final_score,
            "mode":"AUTONOMOUS_24H"
        }


autonomous_core=AutonomousTradingCore()
