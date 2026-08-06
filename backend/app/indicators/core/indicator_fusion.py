class IndicatorFusionEngine:

    def analyze(
        self,
        ema,
        rsi,
        macd,
        atr,
        vwap
    ):

        votes = []
        risk_flags = []

        if ema.get("signal") == "BULLISH":
            votes.append("BUY")

        elif ema.get("signal") == "BEARISH":
            votes.append("SELL")


        if macd.get("signal") == "BULLISH":
            votes.append("BUY_CONFIRM")

        elif macd.get("signal") == "BEARISH":
            votes.append("SELL_CONFIRM")


        if rsi.get("signal") == "OVERBOUGHT":
            risk_flags.append("RSI_OVERBOUGHT")

        elif rsi.get("signal") == "OVERSOLD":
            risk_flags.append("RSI_OVERSOLD")


        if atr.get("signal") == "HIGH_VOLATILITY":
            risk_flags.append("HIGH_VOLATILITY")


        if vwap.get("signal") == "BULLISH":
            votes.append("VWAP_BUY")

        elif vwap.get("signal") == "BEARISH":
            votes.append("VWAP_SELL")


        decision = "WAIT"

        if (
            "BUY" in votes
            and "BUY_CONFIRM" in votes
            and "VWAP_BUY" in votes
            and not risk_flags
        ):
            decision = "BUY"


        elif (
            "SELL" in votes
            and "SELL_CONFIRM" in votes
            and "VWAP_SELL" in votes
            and not risk_flags
        ):
            decision = "SELL"


        return {
            "engine": "INDICATOR_FUSION",
            "decision": decision,
            "votes": votes,
            "risk_flags": risk_flags
        }
