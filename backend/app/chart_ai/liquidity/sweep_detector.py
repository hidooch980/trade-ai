class SweepDetector:

    def analyze(self, candles):

        if len(candles) < 5:
            return {
                "status":"INSUFFICIENT_DATA"
            }

        highs=[c["high"] for c in candles[-5:]]
        lows=[c["low"] for c in candles[-5:]]

        last=candles[-1]

        result={
            "liquidity_grab":False,
            "direction":None
        }

        previous_high=max(highs[:-1])
        previous_low=min(lows[:-1])

        if last["high"] > previous_high and last["close"] < previous_high:
            result["liquidity_grab"]=True
            result["direction"]="BUY_SIDE_SWEEP"

        if last["low"] < previous_low and last["close"] > previous_low:
            result["liquidity_grab"]=True
            result["direction"]="SELL_SIDE_SWEEP"

        return result
