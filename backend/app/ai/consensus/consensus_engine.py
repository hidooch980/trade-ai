class AIConsensusEngine:

    def analyze(
        self,
        reports
    ):

        votes = {
            "BUY": 0,
            "SELL": 0,
            "WAIT": 0
        }

        confidence = 0


        for report in reports:

            signal = report.get("signal")

            if signal in votes:

                votes[signal] += 1

            confidence += report.get(
                "confidence",
                0
            )


        total = len(reports)

        if total:

            confidence = round(
                confidence / total,
                2
            )


        decision = max(
            votes,
            key=votes.get
        )


        return {
            "engine": "AI_CONSENSUS",
            "decision": decision,
            "votes": votes,
            "confidence": confidence
        }
