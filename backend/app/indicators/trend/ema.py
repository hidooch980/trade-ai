class EMAEngine:

    def calculate(self, prices, short_period=9, long_period=21):

        if len(prices) < long_period:
            return {
                "indicator": "EMA",
                "signal": "INSUFFICIENT_DATA",
                "confidence": 0
            }

        def ema(data, period):
            multiplier = 2 / (period + 1)
            value = data[0]

            for price in data[1:]:
                value = (price - value) * multiplier + value

            return round(value, 4)

        short_ema = ema(
            prices[-short_period:],
            short_period
        )

        long_ema = ema(
            prices[-long_period:],
            long_period
        )

        if short_ema > long_ema:
            signal = "BULLISH"
        elif short_ema < long_ema:
            signal = "BEARISH"
        else:
            signal = "NEUTRAL"

        difference = abs(short_ema - long_ema)

        confidence = min(
            round(difference / long_ema * 1000, 2),
            100
        )

        return {
            "indicator": "EMA",
            "short": short_ema,
            "long": long_ema,
            "signal": signal,
            "confidence": confidence
        }
