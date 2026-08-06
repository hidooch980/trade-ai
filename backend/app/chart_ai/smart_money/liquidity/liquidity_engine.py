class LiquidityEngine:

    def analyze(self, candles):

        if len(candles) < 2:
            return {
                "liquidity": "NO_DATA"
            }


        highs = [
            c["high"]
            for c in candles
        ]

        lows = [
            c["low"]
            for c in candles
        ]


        buy_side_liquidity = max(highs)

        sell_side_liquidity = min(lows)


        return {
            "engine": "LIQUIDITY",
            "buy_side": buy_side_liquidity,
            "sell_side": sell_side_liquidity,
            "status": "DETECTED"
        }
