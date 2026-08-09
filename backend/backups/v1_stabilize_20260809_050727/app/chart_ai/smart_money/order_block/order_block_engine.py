class OrderBlockEngine:

    def analyze(self, candles):

        if len(candles) < 3:
            return {
                "order_block": None
            }


        previous = candles[-2]
        current = candles[-1]


        block_type = "NONE"
        zone = None


        if current["close"] > previous["high"]:

            block_type = "BULLISH"

            zone = {
                "high": previous["high"],
                "low": previous["low"]
            }


        elif current["close"] < previous["low"]:

            block_type = "BEARISH"

            zone = {
                "high": previous["high"],
                "low": previous["low"]
            }


        score = 0

        if block_type == "BULLISH":
            score = 20

        elif block_type == "BEARISH":
            score = -20

        return {
            "engine": "ORDER_BLOCK",
            "type": block_type,
            "zone": zone,
            "confidence": 50,
            "score": score
        }
