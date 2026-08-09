from app.decision.ai_ranking_engine import ai_ranking_engine
from app.risk.risk_engine import risk_engine


class FinalTradeDecisionEngine:


    def decide(
        self,
        signals,
        balance=10000
    ):

        ranked = ai_ranking_engine.rank(
            signals
        )


        if not ranked:
            return {
                "decision": "NO_TRADE"
            }


        best = ranked[0]


        decision = best.get(
            "decision"
        )


        if decision not in [
            "BUY",
            "SELL"
        ]:
            return {
                "decision": "WAIT",
                "reason": "weak signal"
            }


        price = best.get(
            "technical",
            {}
        ).get(
            "price",
            0
        )


        risk = risk_engine.calculate(
            balance,
            price,
            best.get(
                "confidence",
                0
            )
        )


        return {

            "symbol": best["symbol"],

            "action": decision,

            "confidence": best.get(
                "confidence"
            ),

            "ai_score": best.get(
                "ai_score"
            ),

            "reasons": best.get(
                "reasons"
            ),

            "risk": risk
        }



final_trade_decision_engine = FinalTradeDecisionEngine()
