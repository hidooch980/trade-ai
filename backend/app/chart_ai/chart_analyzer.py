class ChartAnalyzer:

    def analyze(self, candles):

        return {
            "candles": len(candles),
            "patterns": [],
            "support": None,
            "resistance": None,
            "market_structure": "UNKNOWN"
        }
