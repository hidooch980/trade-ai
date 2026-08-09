class MarketStructureEngine:

    def analyze(self, candles):

        if len(candles) < 5:
            return {
                "status": "INSUFFICIENT_DATA"
            }

        highs = [c["high"] for c in candles[-5:]]
        lows = [c["low"] for c in candles[-5:]]

        bullish = 0
        bearish = 0

        for i in range(1, len(highs)):
            if highs[i] > highs[i-1] and lows[i] >= lows[i-1]:
                bullish += 1

            if highs[i] < highs[i-1] and lows[i] <= lows[i-1]:
                bearish += 1

        result = {
            "trend": "RANGE",
            "structure": None,
            "bos": False,
            "choch": False
        }

        if bullish >= 2:
            result["trend"] = "BULLISH"
            result["structure"] = "HH-HL"
            result["bos"] = True

        elif bearish >= 2:
            result["trend"] = "BEARISH"
            result["structure"] = "LH-LL"
            result["choch"] = True

        return result
