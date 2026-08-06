class ATRRiskCalculator:

    def calculate(
        self,
        entry_price,
        atr_value,
        direction="BUY",
        atr_multiplier=2,
        reward_ratio=2
    ):

        risk_distance = atr_value * atr_multiplier

        if direction == "BUY":

            stop_loss = entry_price - risk_distance
            take_profit = entry_price + (
                risk_distance * reward_ratio
            )

        else:

            stop_loss = entry_price + risk_distance
            take_profit = entry_price - (
                risk_distance * reward_ratio
            )

        return {
            "entry": entry_price,
            "direction": direction,
            "stop_loss": round(stop_loss, 4),
            "take_profit": round(take_profit, 4),
            "risk_reward": reward_ratio,
            "atr_used": atr_value
        }
