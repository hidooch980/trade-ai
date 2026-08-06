class AICommittee:

    def __init__(self):
        self.agents={
            "technical":25,
            "quant":20,
            "smart_money":20,
            "risk":15,
            "macro":10,
            "news":10
        }

    def vote(self,signals):

        score=0
        votes={}

        for agent,weight in self.agents.items():
            signal=signals.get(agent,"WAIT")
            votes[agent]=signal

            if signal=="BUY":
                score+=weight
            elif signal=="SELL":
                score-=weight

        if score>=60:
            decision="BUY"
        elif score<=-60:
            decision="SELL"
        else:
            decision="WAIT"

        return {
            "decision":decision,
            "score":score,
            "votes":votes
        }


ai_committee=AICommittee()
