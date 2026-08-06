class PositionMonitor:

    def check(
        self,
        position,
        current_price
    ):

        status = position["status"]
        result = None


        if status != "OPEN":

            return {
                "status": status,
                "result": None
            }


        if position["side"] == "BUY":

            if current_price >= position["take_profit"]:
                status = "CLOSED"
                result = "WIN"

            elif current_price <= position["stop_loss"]:
                status = "CLOSED"
                result = "LOSS"


        elif position["side"] == "SELL":

            if current_price <= position["take_profit"]:
                status = "CLOSED"
                result = "WIN"

            elif current_price >= position["stop_loss"]:
                status = "CLOSED"
                result = "LOSS"


        return {
            "status": status,
            "result": result,
            "current_price": current_price
        }
