class MACDEngine:

    def calculate(self, prices, fast=12, slow=26, signal_period=9):

        if len(prices) < slow + signal_period:
            return {
                "indicator": "MACD",
                "signal": "INSUFFICIENT_DATA",
                "confidence": 0
            }

        def ema(data, period):
            multiplier = 2 / (period + 1)
            value = data[0]

            for price in data[1:]:
                value = (price - value) * multiplier + value

            return value

        fast_ema = ema(
            prices[-fast:],
            fast
        )

        slow_ema = ema(
            prices[-slow:],
            slow
        )

        macd_value = fast_ema - slow_ema

        signal_value = ema(
            prices[-signal_period:],
            signal_period
        )

        if macd_value > signal_value:
            direction = "BULLISH"
        elif macd_value < signal_value:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"

        confidence = min(
            round(abs(macd_value - signal_value) * 10, 2),
            100
        )

        return {
            "indicator": "MACD",
            "macd": round(macd_value, 4),
            "signal_line": round(signal_value, 4),
            "signal": direction,
            "confidence": confidence
        }
