from app.risk.risk_engine import risk_engine


class FinalTradeEngine:


    def decide(
        self,
        opportunity,
        price
    ):

        if not opportunity:

            return {
                "decision":"WAIT",
                "reason":"NO OPPORTUNITY"
            }


        symbol = opportunity.get("symbol")
        side = opportunity.get("side")
        confidence = opportunity.get("confidence",0)


        if confidence < 50:

            return {
                "decision":"WAIT",
                "symbol":symbol,
                "reason":"LOW CONFIDENCE"
            }


        risk = risk_engine.calculate(
            price,
            side
        )


        if not risk.get("allowed"):

            return {
                "decision":"WAIT",
                "symbol":symbol,
                "reason":risk.get("reason")
            }


        return {

            "decision":"OPEN",

            "symbol":symbol,

            "side":side,

            "confidence":confidence,

            "risk":risk

        }



final_trade_engine = FinalTradeEngine()
