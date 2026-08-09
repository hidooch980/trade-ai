class AIRankingEngine:

    def rank(self, signals):

        ranked = []

        for item in signals:

            score = 0

            confidence = item.get(
                "confidence",
                0
            )

            decision = item.get(
                "decision"
            )

            reasons = item.get(
                "reasons",
                []
            )

            score += confidence

            if decision in [
                "BUY",
                "SELL"
            ]:
                score += 20

            if len(reasons) >= 2:
                score += 10

            item["ai_score"] = score

            ranked.append(item)


        ranked.sort(
            key=lambda x: x["ai_score"],
            reverse=True
        )

        return ranked[:10]


ai_ranking_engine = AIRankingEngine()
