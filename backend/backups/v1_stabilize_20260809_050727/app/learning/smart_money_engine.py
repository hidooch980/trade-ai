class SmartMoneyEngine:


    def analyze(self, candles):

        if len(candles) < 20:
            return {
                "smart_signal": "WAIT",
                "score": 0
            }


        highs = [
            c["high"]
            for c in candles
        ]

        lows = [
            c["low"]
            for c in candles
        ]

        closes = [
            c["close"]
            for c in candles
        ]


        last = closes[-1]

        high20 = max(
            highs[-20:]
        )

        low20 = min(
            lows[-20:]
        )


        score = 0
        reasons = []


        # Liquidity sweep
        if last > high20:
            score += 30
            reasons.append(
                "Liquidity breakout"
            )


        elif last < low20:
            score -= 30
            reasons.append(
                "Liquidity breakdown"
            )


        # Momentum
        avg = sum(
            closes[-20:]
        ) / 20


        if last > avg:
            score += 20
            reasons.append(
                "Institutional buying pressure"
            )

        else:
            score -= 20
            reasons.append(
                "Institutional selling pressure"
            )


        if score >= 30:
            signal = "BUY"

        elif score <= -30:
            signal = "SELL"

        else:
            signal = "WAIT"


        return {
            "smart_signal": signal,
            "score": score,
            "reasons": reasons
        }



smart_money_engine = SmartMoneyEngine()
