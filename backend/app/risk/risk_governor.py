class RiskGovernor:

    def calculate_position_size(
        self,
        capital,
        risk_percent,
        entry_price,
        stop_loss
    ):

        risk_amount = capital * (risk_percent / 100)

        distance = abs(
            entry_price - stop_loss
        )

        if distance == 0:
            return {
                "approved": False,
                "reason": "INVALID_STOP_LOSS"
            }


        volume = risk_amount / distance


        return {
            "approved": True,
            "risk_amount": risk_amount,
            "stop_distance": distance,
            "volume": round(volume, 2),
            "entry_price": entry_price
        }


    def validate_drawdown(
        self,
        current_loss_percent
    ):

        if current_loss_percent >= 10:

            return {
                "approved": False,
                "status": "DRAWDOWN_LIMIT"
            }


        return {
            "approved": True,
            "status": "SAFE"
        }
