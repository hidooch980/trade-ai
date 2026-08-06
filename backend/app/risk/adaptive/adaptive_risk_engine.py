class AdaptiveRiskEngine:


    def calculate(
        self,
        performance,
        base_risk=1
    ):

        win_rate = performance.get(
            "win_rate",
            0
        )

        drawdown = performance.get(
            "max_drawdown",
            0
        )


        risk = base_risk


        if win_rate >= 70:
            risk += 0.5


        if win_rate >= 90:
            risk += 0.5


        if drawdown >= 5:
            risk -= 0.5


        if drawdown >= 10:
            risk -= 0.5


        if risk < 0.5:
            risk = 0.5


        if risk > 3:
            risk = 3


        return {
            "risk_percent": risk,
            "win_rate": win_rate,
            "drawdown": drawdown,
            "status": "ADAPTIVE"
        }


adaptive_risk_engine = AdaptiveRiskEngine()
