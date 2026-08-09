class ConfidenceEngine:

    def calculate(
        self,
        decision,
        score,
        smart_money,
        risk
    ):

        confidence = 0
        reasons = []


        confidence += abs(score)

        if smart_money.get("score",0) >= 30:
            confidence += 15
            reasons.append("SMART_MONEY_CONFIRM")


        if risk.get("approved"):
            confidence += 10
            reasons.append("RISK_OK")


        if decision == "WAIT":
            confidence -= 5
            reasons.append("NO_DIRECTION_PENALTY")


        if confidence >= 80:
            level = "HIGH"

        elif confidence >= 50:
            level = "MEDIUM"

        else:
            level = "LOW"


        return {
            "confidence": confidence,
            "level": level,
            "reasons": reasons,
            "trade_allowed": confidence >= 65
        }


confidence_engine = ConfidenceEngine()
