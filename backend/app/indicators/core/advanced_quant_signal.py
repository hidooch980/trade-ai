class AdvancedQuantSignalEngine:

    def analyze(self, ema, rsi, macd):

        votes = []

        if ema["signal"] == "BULLISH":
            votes.append("BUY")

        elif ema["signal"] == "BEARISH":
            votes.append("SELL")


        if rsi["signal"] == "NORMAL":
            votes.append("MOMENTUM_OK")

        elif rsi["signal"] == "OVERBOUGHT":
            votes.append("RISK_HIGH")

        elif rsi["signal"] == "OVERSOLD":
            votes.append("RISK_HIGH")


        if macd["signal"] == "BULLISH":
            votes.append("BUY_CONFIRM")

        elif macd["signal"] == "BEARISH":
            votes.append("SELL_CONFIRM")


        decision = "WAIT"

        if (
            "BUY" in votes
            and "BUY_CONFIRM" in votes
            and "RISK_HIGH" not in votes
        ):
            decision = "BUY"

        elif (
            "SELL" in votes
            and "SELL_CONFIRM" in votes
            and "RISK_HIGH" not in votes
        ):
            decision = "SELL"


        confidence = round(
            (
                ema.get("confidence",0)
                +
                rsi.get("confidence",0)
                +
                macd.get("confidence",0)
            ) / 3,
            2
        )

        return {
            "engine": "ADVANCED_QUANT",
            "decision": decision,
            "confidence": confidence,
            "votes": votes
        }
