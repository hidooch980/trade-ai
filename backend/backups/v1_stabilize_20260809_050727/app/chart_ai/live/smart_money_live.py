from app.chart_ai.structure.market_structure import MarketStructureEngine
from app.chart_ai.liquidity.liquidity_engine import LiquidityEngine
from app.market.universe.symbol_universe import canonical, category


class SmartMoneyLive:
    def __init__(self):
        self.structure = MarketStructureEngine()
        self.liquidity = LiquidityEngine()

    def analyze(self, candles, symbol=None):
        symbol = canonical(symbol) if symbol else None

        if len(candles) < 3:
            return {
                "symbol": symbol,
                "category": category(symbol) if symbol else "OTHER",
                "status": "INSUFFICIENT_DATA",
                "decision": "WAIT",
                "score": 0,
                "reasons": ["INSUFFICIENT_DATA"]
            }

        last = candles[-1]
        prev = candles[-2]

        structure = self.structure.analyze(candles)
        liquidity = self.liquidity.analyze(candles)

        score = 0
        reasons = []

        trend = structure.get("trend")

        if trend == "BULLISH":
            score += 30
            reasons.append("BULLISH_STRUCTURE")
        elif trend == "BEARISH":
            score -= 30
            reasons.append("BEARISH_STRUCTURE")

        if liquidity.get("buy_side_liquidity"):
            reasons.append("BUY_SIDE_LIQUIDITY")

        if liquidity.get("sell_side_liquidity"):
            score -= 5
            reasons.append("SELL_SIDE_LIQUIDITY")

        bos = False
        choch = False
        sweep = False

        if last["high"] > prev["high"]:
            bos = True

        if last["low"] < prev["low"]:
            choch = True

        if last["high"] > prev["high"] and last["close"] < prev["high"]:
            sweep = True
            score -= 10
            reasons.append("BEARISH_LIQUIDITY_SWEEP")

        if last["low"] < prev["low"] and last["close"] > prev["low"]:
            sweep = True
            score += 10
            reasons.append("BULLISH_LIQUIDITY_SWEEP")

        if score >= 45:
            decision = "BUY"
        elif score <= -45:
            decision = "SELL"
        else:
            decision = "WAIT"

        return {
            "symbol": symbol,
            "category": category(symbol) if symbol else "OTHER",
            "status": "OK",
            "decision": decision,
            "score": score,
            "reasons": reasons,
            "market_structure": structure,
            "liquidity_analysis": liquidity,
            "trend": trend or "RANGE",
            "bos": bos,
            "choch": choch,
            "liquidity_sweep": sweep
        }
