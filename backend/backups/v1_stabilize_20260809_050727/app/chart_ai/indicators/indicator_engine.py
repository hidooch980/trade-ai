class IndicatorEngine:

    def analyze(self, candles):

        if len(candles) < 5:
            return {
                "trend":"NEUTRAL",
                "momentum":"NEUTRAL",
                "volatility":"LOW",
                "volume":"NORMAL",
                "pattern":"NONE",
                "score":0
            }

        closes=[c["close"] for c in candles]

        score=0
        reasons=[]


        # Trend EMA logic
        fast=sum(closes[-5:])/5
        slow=sum(closes)/len(closes)

        if fast > slow:
            trend="BULLISH"
            score+=20
            reasons.append("EMA_TREND_UP")

        elif fast < slow:
            trend="BEARISH"
            score-=20
            reasons.append("EMA_TREND_DOWN")

        else:
            trend="NEUTRAL"


        # Momentum
        change=closes[-1]-closes[-5]

        if change > 0:
            momentum="BUY"
            score+=10
            reasons.append("MOMENTUM_BUY")

        elif change < 0:
            momentum="SELL"
            score-=10
            reasons.append("MOMENTUM_SELL")

        else:
            momentum="NEUTRAL"


        # Volatility
        high=max(c["high"] for c in candles[-10:])
        low=min(c["low"] for c in candles[-10:])

        range_value=high-low

        if range_value > abs(closes[-1])*0.002:
            volatility="HIGH"
            reasons.append("HIGH_VOLATILITY")

        else:
            volatility="LOW"


        # Volume
        volumes=[c.get("volume",0) for c in candles]

        if volumes[-1] > sum(volumes)/len(volumes):
            volume="HIGH"
            score+=10
            reasons.append("VOLUME_CONFIRMATION")

        else:
            volume="NORMAL"


        # Simple MTR reversal detection
        pattern="NONE"

        if closes[-3] < closes[-2] and closes[-2] > closes[-1]:
            pattern="MTR_SELL"
            score-=15
            reasons.append("MTR_REVERSAL_SELL")


        elif closes[-3] > closes[-2] and closes[-2] < closes[-1]:
            pattern="MTR_BUY"
            score+=15
            reasons.append("MTR_REVERSAL_BUY")


        return {
            "trend":trend,
            "momentum":momentum,
            "volatility":volatility,
            "volume":volume,
            "pattern":pattern,
            "score":score,
            "reasons":reasons
        }


indicator_engine=IndicatorEngine()
