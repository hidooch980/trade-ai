class FVGEngine:

    def analyze(self, candles):

        if len(candles) < 3:
            return {
                "fvg": None
            }

        first = candles[-3]
        last = candles[-1]

        gaps = []

        if first["high"] < last["low"]:
            gaps.append({
                "type": "BULLISH",
                "high": last["low"],
                "low": first["high"]
            })

        elif first["low"] > last["high"]:
            gaps.append({
                "type": "BEARISH",
                "high": first["low"],
                "low": last["high"]
            })

        return {
            "engine": "FVG",
            "gaps": gaps,
            "detected": len(gaps) > 0
        }
