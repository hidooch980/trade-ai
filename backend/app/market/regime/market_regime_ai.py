import statistics


class MarketRegimeAI:

    def analyze(self, candles):

        if len(candles) < 20:
            return {
                "regime": "UNKNOWN",
                "confidence": 0
            }

        closes = [
            c.get("close",0)
            for c in candles[-20:]
        ]

        change = closes[-1] - closes[0]

        volatility = statistics.mean(
            [
                abs(closes[i]-closes[i-1])
                for i in range(1,len(closes))
            ]
        )

        if volatility > closes[-1] * 0.01:
            regime = "VOLATILE"

        elif abs(change) > closes[-1] * 0.005:
            regime = "TREND"

        else:
            regime = "RANGE"


        return {
            "regime": regime,
            "confidence": round(min(abs(change)+volatility,100),2),
            "change": change,
            "volatility": volatility
        }


market_regime_ai = MarketRegimeAI()
