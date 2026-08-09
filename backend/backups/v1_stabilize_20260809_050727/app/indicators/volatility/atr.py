class ATREngine:

    def calculate(self, candles, period=14):

        if len(candles) <= period:
            return {
                "indicator": "ATR",
                "value": 0,
                "signal": "INSUFFICIENT_DATA",
                "confidence": 0
            }

        true_ranges = []

        for i in range(1, len(candles)):

            high = candles[i]["high"]
            low = candles[i]["low"]
            previous_close = candles[i-1]["close"]

            tr = max(
                high - low,
                abs(high - previous_close),
                abs(low - previous_close)
            )

            true_ranges.append(tr)

        atr = sum(true_ranges[-period:]) / period

        return {
            "indicator": "ATR",
            "value": round(atr, 4),
            "signal": "HIGH_VOLATILITY" if atr > 10 else "NORMAL",
            "confidence": round(min(atr * 5, 100), 2)
        }
