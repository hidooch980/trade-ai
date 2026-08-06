class SmartMoneyEntryScore:

    def calculate(
        self,
        structure,
        liquidity,
        order_block,
        fvg
    ):

        score = 0
        reasons = []


        if structure.get("structure") == "UPTREND":
            score += 25
            reasons.append("UPTREND")


        if liquidity.get("status") == "DETECTED":
            score += 25
            reasons.append("LIQUIDITY")


        if order_block.get("type") == "BULLISH":
            score += 25
            reasons.append("BULLISH_ORDER_BLOCK")


        if fvg.get("detected"):

            score += 25
            reasons.append("FVG")


        decision = "WAIT"

        if score >= 75:
            decision = "BUY"

        elif score <= 25:
            decision = "SELL"


        return {
            "engine": "SMART_MONEY_SCORE",
            "score": score,
            "decision": decision,
            "reasons": reasons
        }
