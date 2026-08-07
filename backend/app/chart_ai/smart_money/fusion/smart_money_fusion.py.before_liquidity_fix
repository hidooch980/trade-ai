from app.chart_ai.indicators.advanced_indicators import advanced_indicators


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

        indicator = advanced_indicators.analyze(
            candles
        )

        indicator_score = indicator.get(
            "score",
            0
        )

        score += indicator_score

        reasons.extend(
            indicator.get(
                "reasons",
                []
            )
        )

        trend = structure.get("trend")

        if trend == "BULLISH":
            score += 30
            reasons.append("BULLISH_STRUCTURE")

        elif trend == "BEARISH":
            score -= 30
            reasons.append("BEARISH_STRUCTURE")


        if liquidity.get("buy_side_liquidity"):
            reasons.append("BUY_SIDE_LIQUIDITY")

        if liquidity.get("sell_side_liquidity"):
            score -= 5
            reasons.append("SELL_SIDE_LIQUIDITY")


        ob_type = order_block.get("type")

        if ob_type == "BULLISH":
            score += 25
            reasons.append("BULLISH_ORDER_BLOCK")

        elif ob_type == "BEARISH":
            score -= 25
            reasons.append("BEARISH_ORDER_BLOCK")


        if fvg.get("detected"):

            gaps = fvg.get("gaps", [])

            if gaps:
                gap_type = gaps[-1].get("type")

                if gap_type == "BULLISH":
                    score += 15
                    reasons.append("BULLISH_FVG")

                elif gap_type == "BEARISH":
                    score -= 15
                    reasons.append("BEARISH_FVG")


        if sweep.get("liquidity_grab"):

            direction = sweep.get("direction")

            if direction == "BUY":
                score += 20
                reasons.append("BUY_SWEEP")

            elif direction == "SELL":
                score -= 20
                reasons.append("SELL_SWEEP")


        decision = "WAIT"

        if score >= 45:
            decision = "BUY"

        elif score <= -60:
            decision = "SELL"


        return {
            "decision": decision,
            "score": score,
            "reasons": reasons
        }
