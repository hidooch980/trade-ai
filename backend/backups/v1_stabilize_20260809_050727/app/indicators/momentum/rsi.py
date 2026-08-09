class RSIEngine:

    def calculate(self, prices, period=14):

        if len(prices) <= period:
            return {
                "indicator": "RSI",
                "value": 0,
                "signal": "INSUFFICIENT_DATA",
                "confidence": 0
            }

        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]

            if change >= 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        rsi = round(rsi, 2)

        if rsi >= 70:
            signal = "OVERBOUGHT"
        elif rsi <= 30:
            signal = "OVERSOLD"
        else:
            signal = "NORMAL"

        confidence = abs(50 - rsi) * 2

        return {
            "indicator": "RSI",
            "value": rsi,
            "signal": signal,
            "confidence": round(min(confidence, 100), 2)
        }
