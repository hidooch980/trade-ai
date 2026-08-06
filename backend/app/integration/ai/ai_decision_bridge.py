class AIDecisionBridge:

    def combine(
        self,
        consensus,
        final_signal
    ):

        final_signal["ai_consensus"] = consensus


        if consensus.get("decision") == "BUY":

            final_signal["confidence"] += (
                consensus.get("confidence", 0) / 10
            )


        elif consensus.get("decision") == "SELL":

            final_signal["confidence"] -= (
                consensus.get("confidence", 0) / 10
            )


        return final_signal
