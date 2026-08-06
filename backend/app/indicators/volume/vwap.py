class VWAPEngine:

    def calculate(self, candles):

        if not candles:
            return {
                "indicator": "VWAP",
                "value": 0,
                "signal": "NO_DATA"
            }

        total_volume = 0
        total_value = 0

        for candle in candles:

            typical_price = (
                candle["high"]
                +
                candle["low"]
                +
                candle["close"]
            ) / 3

            volume = candle.get(
                "volume",
                0
            )

            total_value += (
                typical_price * volume
            )

            total_volume += volume


        if total_volume == 0:
            return {
                "indicator": "VWAP",
                "value": 0,
                "signal": "NO_VOLUME"
            }


        vwap = total_value / total_volume

        last_price = candles[-1]["close"]

        if last_price > vwap:
            signal = "BULLISH"

        elif last_price < vwap:
            signal = "BEARISH"

        else:
            signal = "NEUTRAL"


        return {
            "indicator": "VWAP",
            "value": round(vwap,4),
            "last_price": last_price,
            "signal": signal
        }
