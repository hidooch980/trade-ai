from app.chart_ai.structure.market_structure import MarketStructureEngine
from app.chart_ai.liquidity.liquidity_engine import LiquidityEngine


class SmartMoneyLive:

    def analyze(self, candles):

        if len(candles) < 3:
            return {
                "status": "INSUFFICIENT_DATA"
            }


        last = candles[-1]
        prev = candles[-2]


        structure = self.structure.analyze(candles)
        liquidity = self.liquidity.analyze(candles)

        result = {
            "market_structure": structure,
            "liquidity_analysis": liquidity,
            "trend": "RANGE",
            "bos": False,
            "choch": False,
            "liquidity_sweep": False
        }


        if last["high"] > prev["high"]:

            result["trend"] = "BULLISH"
            result["bos"] = True


        elif last["low"] < prev["low"]:

            result["trend"] = "BEARISH"
            result["choch"] = True


        if last["high"] > prev["high"] and last["close"] < prev["high"]:

            result["liquidity_sweep"] = True


        return result
