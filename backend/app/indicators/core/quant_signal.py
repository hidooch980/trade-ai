class QuantSignalEngine:

    def analyze(self, ema_result, rsi_result):

        ema_signal = ema_result.get("signal")
        rsi_signal = rsi_result.get("signal")

        decision = "WAIT"
        reasons = []

        if ema_signal == "BULLISH":

            if rsi_signal == "NORMAL":
                decision = "BUY"
                reasons.append("trend_confirmed")

            elif rsi_signal == "OVERBOUGHT":
                reasons.append("overbought_filter")

        elif ema_signal == "BEARISH":

            if rsi_signal == "NORMAL":
                decision = "SELL"
                reasons.append("trend_confirmed")

            elif rsi_signal == "OVERSOLD":
                reasons.append("oversold_filter")

        confidence = (
            ema_result.get("confidence", 0)
            +
            rsi_result.get("confidence", 0)
        ) / 2

        return {
            "engine": "QUANT_SIGNAL",
            "decision": decision,
            "confidence": round(confidence, 2),
            "reasons": reasons
        }
