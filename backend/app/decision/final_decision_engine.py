class FinalDecisionEngine:

    def decide(
        self,
        indicator_signal,
        ai_signal,
        risk,
        smart_money
    ):

        score = 0
        reasons = []

        if indicator_signal.get("decision") == "BUY":
            score += 25
            reasons.append("INDICATORS_BUY")

        if ai_signal.get("decision") == "BUY":
            score += 25
            reasons.append("AI_BUY")

        if risk.get("approved"):
            score += 25
            reasons.append("RISK_APPROVED")

        if smart_money.get("decision") == "BUY":
            score += 25
            reasons.append("SMART_MONEY_BUY")

        decision = "WAIT"

        if score >= 75:
            decision = "BUY"

        elif score <= 25:
            decision = "SELL"

        return {
            "engine": "FINAL_DECISION",
            "decision": decision,
            "score": score,
            "reasons": reasons
        }
