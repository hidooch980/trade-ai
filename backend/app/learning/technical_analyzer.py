import json
import os
import statistics


class TechnicalAnalyzer:

    def __init__(self):
        self.file = "app/learning/data/market_data.json"


    def get_candles(self, symbol):

        if not os.path.exists(self.file):
            return []

        with open(self.file, "r") as f:
            data = json.load(f)

        candles = []

        for item in data:
            if (
                item.get("symbol") == symbol
                and "close" in item.get("data", {})
            ):
                candles.append(item["data"])

        return candles[-100:]


    def calculate(self, symbol):

        candles = self.get_candles(symbol)

        if len(candles) < 20:
            return {
                "symbol": symbol,
                "signal": "WAIT",
                "score": 0,
                "reason": "not enough data"
            }


        closes = [
            float(c["close"])
            for c in candles
        ]

        current = closes[-1]

        sma20 = sum(closes[-20:]) / 20


        gains = []
        losses = []

        for i in range(1,len(closes)):

            diff = closes[i]-closes[i-1]

            if diff >= 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))


        avg_gain = statistics.mean(gains) if gains else 0
        avg_loss = statistics.mean(losses) if losses else 1


        rs = avg_gain / avg_loss

        rsi = 100 - (100/(1+rs))


        score = 0
        reasons = []


        if current > sma20:
            score += 30
            reasons.append("ABOVE_SMA20")

        else:
            score -= 30
            reasons.append("BELOW_SMA20")


        if rsi < 30:
            score += 25
            reasons.append("RSI_OVERSOLD")

        elif rsi > 70:
            score -= 25
            reasons.append("RSI_OVERBOUGHT")


        if closes[-1] > closes[-5]:
            score += 15
            reasons.append("MOMENTUM_UP")

        else:
            score -= 15
            reasons.append("MOMENTUM_DOWN")


        signal = "WAIT"

        if score >= 40:
            signal = "BUY"

        elif score <= -40:
            signal = "SELL"


        return {
            "symbol": symbol,
            "price": current,
            "sma20": round(sma20,5),
            "rsi": round(rsi,2),
            "score": score,
            "signal": signal,
            "reasons": reasons
        }


technical_analyzer = TechnicalAnalyzer()
