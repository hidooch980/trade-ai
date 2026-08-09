import json
import os

from app.market.universe.symbol_universe import canonical, category


class SmartMoneyEngine:
    def __init__(self):
        self.file = "app/learning/data/market_data.json"

    def get_market_data(self, symbol):
        if not os.path.exists(self.file):
            return []

        target = canonical(symbol)

        try:
            with open(self.file) as f:
                data = json.load(f)
        except Exception:
            return []

        result = []

        for x in data:
            raw_symbol = x.get("symbol")
            if canonical(raw_symbol) == target:
                result.append(x.get("data", {}))

        return result

    def analyze(self, symbol):
        target = canonical(symbol)
        market_type = category(target)
        data = self.get_market_data(target)

        # No external historical smart-money dataset:
        # keep the signal neutral instead of UNKNOWN so the chart/live
        # Smart Money engine remains the primary source.
        if len(data) < 5:
            return {
                "symbol": target,
                "category": market_type,
                "smart_money": "NEUTRAL",
                "score": 0,
                "reasons": ["NO_MARKET_HISTORY"]
            }

        latest = data[-1]

        score = 0
        reasons = []

        volume = latest.get("volume")

        if isinstance(volume, (int, float)) and volume > 0:
            volumes = [
                x.get("volume", 0)
                for x in data[-20:]
                if isinstance(x.get("volume"), (int, float))
                and x.get("volume", 0) > 0
            ]

            if volumes:
                avg_volume = sum(volumes) / len(volumes)

                if avg_volume > 0 and volume > avg_volume * 1.5:
                    score += 30
                    reasons.append("HIGH_VOLUME_ACTIVITY")

        change = latest.get("change_24h", 0)

        if isinstance(change, (int, float)):
            if change > 2:
                score += 20
                reasons.append("STRONG_ACCUMULATION")
            elif change < -2:
                score -= 20
                reasons.append("DISTRIBUTION_PRESSURE")

        if score >= 30:
            signal = "ACCUMULATION"
        elif score <= -30:
            signal = "DISTRIBUTION"
        else:
            signal = "NEUTRAL"

        return {
            "symbol": target,
            "category": market_type,
            "smart_money": signal,
            "score": score,
            "reasons": reasons
        }


smart_money_engine = SmartMoneyEngine()
