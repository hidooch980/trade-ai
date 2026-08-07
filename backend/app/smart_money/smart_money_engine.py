import json
import os


class SmartMoneyEngine:


    def __init__(self):
        self.file = "app/learning/data/market_data.json"


    def get_market_data(self, symbol):

        if not os.path.exists(self.file):
            return []

        with open(self.file, "r") as f:
            data = json.load(f)

        return [
            x["data"]
            for x in data
            if x.get("symbol") == symbol
        ]


    def analyze(self, symbol):

        data = self.get_market_data(symbol)


        if len(data) < 5:
            return {
                "symbol": symbol,
                "smart_money": "UNKNOWN",
                "score": 0
            }


        latest = data[-1]


        score = 0
        reasons = []


        volume = latest.get("volume")


        if volume:

            volumes = [
                x.get("volume",0)
                for x in data[-20:]
                if x.get("volume")
            ]


            if volumes:

                avg_volume = sum(volumes) / len(volumes)


                if volume > avg_volume * 1.5:
                    score += 30
                    reasons.append(
                        "High volume activity"
                    )


        change = latest.get(
            "change_24h",
            0
        )


        if change > 2:
            score += 20
            reasons.append(
                "Strong accumulation"
            )


        elif change < -2:
            score -= 20
            reasons.append(
                "Distribution pressure"
            )


        if score >= 30:
            signal = "ACCUMULATION"

        elif score <= -30:
            signal = "DISTRIBUTION"

        else:
            signal = "NEUTRAL"


        return {
            "symbol": symbol,
            "smart_money": signal,
            "score": score,
            "reasons": reasons
        }



smart_money_engine = SmartMoneyEngine()
