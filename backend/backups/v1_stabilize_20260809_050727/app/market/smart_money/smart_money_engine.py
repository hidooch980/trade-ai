from typing import List, Dict


class SmartMoneyEngine:

    def detect_structure(self, prices: List[float]) -> Dict:

        if len(prices) < 5:
            return {
                "trend": "UNKNOWN",
                "structure": "INSUFFICIENT_DATA"
            }

        recent = prices[-5:]

        if recent[-1] > max(recent[:-1]):
            trend = "BULLISH"
            structure = "BREAK_OF_STRUCTURE_UP"

        elif recent[-1] < min(recent[:-1]):
            trend = "BEARISH"
            structure = "BREAK_OF_STRUCTURE_DOWN"

        else:
            trend = "RANGE"
            structure = "CONSOLIDATION"

        return {
            "trend": trend,
            "structure": structure
        }


    def liquidity_zone(self, prices: List[float]) -> Dict:

        if len(prices) < 10:
            return {}

        high = max(prices[-10:])
        low = min(prices[-10:])

        return {
            "buy_liquidity": low,
            "sell_liquidity": high
        }
