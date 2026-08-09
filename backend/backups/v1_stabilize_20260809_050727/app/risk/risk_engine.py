class RiskEngine:


    def calculate(
        self,
        price,
        signal,
        balance=10000,
        risk_percent=1
    ):

        risk_amount = (
            balance *
            risk_percent /
            100
        )


        if signal == "BUY":

            stop_loss = price * 0.98
            take_profit = price * 1.04


        elif signal == "SELL":

            stop_loss = price * 1.02
            take_profit = price * 0.96


        else:

            return {
                "allowed": False,
                "reason": "NO SIGNAL"
            }


        distance = abs(
            price - stop_loss
        )


        if distance == 0:

            return {
                "allowed": False,
                "reason": "INVALID PRICE"
            }


        volume = round(
            risk_amount / distance,
            4
        )


        return {
            "allowed": True,
            "risk_amount": risk_amount,
            "entry": price,
            "stop_loss": round(stop_loss,5),
            "take_profit": round(take_profit,5),
            "volume": volume
        }



risk_engine = RiskEngine()
