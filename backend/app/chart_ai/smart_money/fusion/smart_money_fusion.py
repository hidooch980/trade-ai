class SmartMoneyFusion:

    def analyze(
        self,
        candles,
        structure,
        liquidity,
        order_block,
        fvg,
        sweep
    ):

        score = 0
        reasons = []

        if structure.get("trend") == "BULLISH":
            score += 30
            reasons.append("BULLISH_STRUCTURE")

        if liquidity.get("sweep"):
            score += 25
            reasons.append("LIQUIDITY_SWEEP")

        if liquidity.get("buy_side_liquidity"):
            score += 5
            reasons.append("BUY_SIDE_LIQUIDITY")

        if liquidity.get("sell_side_liquidity"):
            score -= 5
            reasons.append("SELL_SIDE_LIQUIDITY")

        if order_block.get("type") == "BULLISH":
            score += 20
            reasons.append("BULLISH_ORDER_BLOCK")

        if fvg.get("detected"):
            score += 15
            reasons.append("FVG_CONFIRMED")

        if sweep.get("liquidity_grab"):
            score += 25
            reasons.append(
                sweep.get("direction")
            )

        decision = "WAIT"

        if score >= 70:
            decision = "BUY"
        elif score <= 30:
            decision = "SELL"

        return {
            "decision": decision,
            "score": score,
            "reasons": reasons
        }
