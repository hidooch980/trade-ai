class MarketStructureEngine:

    def analyze(self, candles):

        if len(candles) < 3:
            return {
                "status": "INSUFFICIENT_DATA"
            }

        prev = candles[-2]
        last = candles[-1]

        result = {
            "trend": "RANGE",
            "structure": None,
            "bos": False,
            "choch": False
        }


        if last["high"] > prev["high"] and last["low"] > prev["low"]:

            result["trend"] = "BULLISH"
            result["structure"] = "HH-HL"


        elif last["high"] < prev["high"] and last["low"] < prev["low"]:

            result["trend"] = "BEARISH"
            result["structure"] = "LH-LL"


        if last["high"] > prev["high"]:
            result["bos"] = True


        if last["low"] < prev["low"]:
            result["choch"] = True


        return result
