from typing import Dict


class MacroEngine:

    def analyze(self, data: Dict) -> Dict:

        interest_rate = data.get("interest_rate", 0)
        inflation = data.get("inflation", 0)
        sentiment = data.get("sentiment", "neutral")

        score = 50

        if inflation > 5:
            score -= 10

        if interest_rate > 4:
            score -= 5

        if sentiment == "positive":
            score += 10

        if sentiment == "negative":
            score -= 10

        return {
            "macro_score": score,
            "risk_level": (
                "HIGH" if score < 40 else "NORMAL"
            )
        }
