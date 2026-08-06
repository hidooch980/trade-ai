from typing import List, Dict


class NewsEngine:

    def analyze(self, news: List[Dict]) -> Dict:

        if not news:
            return {
                "sentiment": "neutral",
                "score": 50,
                "risk": "LOW"
            }

        positive = 0
        negative = 0
        high_impact = 0

        for item in news:

            sentiment = item.get(
                "sentiment",
                "neutral"
            )

            impact = item.get(
                "impact",
                "low"
            )

            if sentiment == "positive":
                positive += 1

            elif sentiment == "negative":
                negative += 1

            if impact == "high":
                high_impact += 1


        score = 50 + (
            positive * 10
        ) - (
            negative * 10
        )


        return {
            "sentiment":
                "positive" if score > 55
                else "negative" if score < 45
                else "neutral",

            "score": score,

            "risk":
                "HIGH" if high_impact > 0
                else "LOW"
        }
