class SupportResistanceEngine:

    def analyze(self, candles):

        if not candles:
            return {
                "support": None,
                "resistance": None
            }


        highs = [
            c["high"]
            for c in candles
        ]

        lows = [
            c["low"]
            for c in candles
        ]


        resistance = max(highs)
        support = min(lows)


        return {
            "support": support,
            "resistance": resistance,
            "range": resistance - support
        }
