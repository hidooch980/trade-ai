class AICommittee:
    def analyze(self,market):
        agents={
            "quant_ai":75,
            "smart_money_ai":80,
            "risk_ai":90,
            "macro_ai":70,
            "news_ai":85
        }
        score=sum(agents.values())//len(agents)
        decision="BUY" if score>=75 else "WAIT"
        return {"decision":decision,"score":score,"agents":agents}

ai_committee=AICommittee()
