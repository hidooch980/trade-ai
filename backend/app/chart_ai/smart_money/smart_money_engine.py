class SmartMoneyEngine:

    def analyze(
        self,
        structure,
        candles
    ):

        signal = "WAIT"

        if structure.get("structure") == "UPTREND":
            signal = "ACCUMULATION"

        elif structure.get("structure") == "DOWNTREND":
            signal = "DISTRIBUTION"


        return {
            "engine": "SMART_MONEY",
            "signal": signal,
            "structure": structure.get("structure"),
            "liquidity": "UNKNOWN",
            "confidence": 50
        }
