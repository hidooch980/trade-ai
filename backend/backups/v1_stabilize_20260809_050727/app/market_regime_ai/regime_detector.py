class MarketRegimeAI:

    def detect(self,market):

        volatility=market.get("volatility",0)
        trend=market.get("trend","UNKNOWN")
        volume=market.get("volume",0)

        if volatility>80:
            regime="HIGH_VOLATILITY"

        elif trend in ["BULLISH","BEARISH"] and volume>0:
            regime="TREND"

        elif volume>0:
            regime="RANGE"

        else:
            regime="UNKNOWN"

        return {
            "regime":regime,
            "volatility":volatility,
            "trend":trend,
            "recommended_mode":self.mode(regime)
        }


    def mode(self,regime):

        modes={
            "TREND":"FOLLOW_TREND",
            "RANGE":"SCALPING",
            "HIGH_VOLATILITY":"DEFENSIVE",
            "UNKNOWN":"WAIT"
        }

        return modes.get(regime,"WAIT")


regime_ai=MarketRegimeAI()
