class RiskDecisionBridge:

    def validate(
        self,
        decision,
        risk_result
    ):

        if decision.get("decision") not in [
            "BUY",
            "SELL"
        ]:

            return {
                "approved": False,
                "reason": "NO_TRADE_SIGNAL"
            }


        if not risk_result.get("approved"):

            return {
                "approved": False,
                "reason": "RISK_REJECTED"
            }


        return {
            "approved": True,
            "decision": decision,
            "risk": risk_result
        }
