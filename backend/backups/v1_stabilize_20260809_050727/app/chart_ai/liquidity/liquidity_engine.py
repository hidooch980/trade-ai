class LiquidityEngine:

    def analyze(self, candles):

        if len(candles) < 3:
            return {
                "status": "INSUFFICIENT_DATA"
            }

        prev = candles[-2]
        last = candles[-1]

        result = {
            "buy_side_liquidity": False,
            "sell_side_liquidity": False,
            "equal_high": False,
            "equal_low": False,
            "sweep": False,
            "direction": None
        }


        # Equal High
        if abs(last["high"] - prev["high"]) <= 2:
            result["equal_high"] = True
            result["buy_side_liquidity"] = True


        # Equal Low
        if abs(last["low"] - prev["low"]) <= 2:
            result["equal_low"] = True
            result["sell_side_liquidity"] = True


        # Buy-side liquidity sweep
        if last["high"] > prev["high"] and last["close"] < prev["high"]:
            result["sweep"] = True
            result["direction"] = "BUY_SIDE"


        # Sell-side liquidity sweep
        if last["low"] < prev["low"] and last["close"] > prev["low"]:
            result["sweep"] = True
            result["direction"] = "SELL_SIDE"


        return result
