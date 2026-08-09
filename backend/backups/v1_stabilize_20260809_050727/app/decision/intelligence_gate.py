class IntelligenceGate:

    def __init__(self):
        self.min_score = 60
        self.min_confidence = 50

    def evaluate(
        self,
        decision_result,
        ai_result,
        smart_money,
        risk
    ):

        score = decision_result.get("score",0)
        decision = decision_result.get("decision","WAIT")

        confidence = ai_result.get(
            "confidence",
            abs(score)
        )

        reasons = []

        if not risk.get("approved"):
            return {
                "decision":"WAIT",
                "approved":False,
                "reason":"RISK_BLOCK"
            }

        if confidence < self.min_confidence:
            return {
                "decision":"WAIT",
                "approved":False,
                "reason":"LOW_CONFIDENCE"
            }

        if smart_money.get("score",0) == 0:
            reasons.append("NO_SMART_MONEY_CONFIRMATION")

        if decision == "BUY":

            if score >= self.min_score:
                reasons.append("BUY_CONFIRMED")

                return {
                    "decision":"BUY",
                    "approved":True,
                    "score":score,
                    "reasons":reasons
                }

        if decision == "SELL":

            if score <= -self.min_score:
                reasons.append("SELL_CONFIRMED")

                return {
                    "decision":"SELL",
                    "approved":True,
                    "score":score,
                    "reasons":reasons
                }


        return {
            "decision":"WAIT",
            "approved":False,
            "score":score,
            "reason":"SIGNAL_NOT_STRONG"
        }


intelligence_gate = IntelligenceGate()
