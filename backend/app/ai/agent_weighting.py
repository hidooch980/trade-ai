class AgentWeightingEngine:

    DEFAULT_WEIGHTS = {
        "Quant AI": 0.30,
        "Smart Money AI": 0.25,
        "Risk AI": 0.25,
        "Macro AI": 0.10,
        "News AI": 0.10
    }


    def calculate(self, reports):

        scores = {
            "BUY": 0,
            "SELL": 0,
            "WAIT": 0
        }


        for report in reports:

            agent = report.get("agent")
            signal = report.get("signal")

            weight = self.DEFAULT_WEIGHTS.get(
                agent,
                0
            )

            if signal in scores:
                scores[signal] += weight


        decision = max(
            scores,
            key=scores.get
        )


        confidence = round(
            scores[decision] * 100,
            2
        )


        return {
            "decision": decision,
            "confidence": confidence,
            "weighted_scores": scores
        }
