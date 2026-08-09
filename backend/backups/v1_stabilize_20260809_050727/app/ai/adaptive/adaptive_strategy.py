from app.ai.performance.performance_analyzer import performance_analyzer


class AdaptiveStrategy:

    def adjust(self, trades):

        performance = performance_analyzer.analyze(
            trades
        )

        win_rate = performance.get(
            "win_rate",
            0
        )

        if win_rate >= 70:
            mode = "AGGRESSIVE"
            weight = 1.2

        elif win_rate >= 50:
            mode = "BALANCED"
            weight = 1.0

        else:
            mode = "DEFENSIVE"
            weight = 0.7


        return {
            "mode": mode,
            "weight": weight,
            "performance": performance
        }


adaptive_strategy = AdaptiveStrategy()
