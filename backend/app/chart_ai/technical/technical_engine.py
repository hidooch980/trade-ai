class TechnicalEngine:

    def analyze(self, candles):

        if len(candles) < 3:
            return {
                "trend": "NEUTRAL",
                "score": 0,
                "reasons": ["NOT_ENOUGH_DATA"]
            }

        closes = [
            c.get("close")
            for c in candles
        ]

        last = closes[-1]
        previous = closes[-2]

        score = 0
        reasons = []

        # Trend
        if last > previous:
            score += 20
            reasons.append("PRICE_RISING")

        elif last < previous:
            score -= 20
            reasons.append("PRICE_FALLING")


        # Momentum ساده
        change = last - closes[0]

        if change > 0:
            score += 15
            reasons.append("MOMENTUM_BUY")

        elif change < 0:
            score -= 15
            reasons.append("MOMENTUM_SELL")


        # Moving average ساده
        ma = sum(closes) / len(closes)

        if last > ma:
            score += 15
            reasons.append("ABOVE_MA")

        else:
            score -= 15
            reasons.append("BELOW_MA")


        trend = "NEUTRAL"

        if score >= 30:
            trend = "BULLISH"

        elif score <= -30:
            trend = "BEARISH"


        return {
            "trend": trend,
            "score": score,
            "price": last,
            "moving_average": ma,
            "reasons": reasons
        }


technical_engine = TechnicalEngine()
