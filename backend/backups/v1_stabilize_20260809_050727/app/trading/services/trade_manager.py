from app.trading.models.position import Position


class TradeManager:

    def open_trade(
        self,
        symbol,
        decision,
        price,
        volume
    ):

        if decision not in ["BUY", "SELL"]:
            return {
                "status": "REJECTED",
                "reason": "NO_TRADE_SIGNAL"
            }


        if decision == "BUY":

            stop_loss = price - 20
            take_profit = price + 40

        else:

            stop_loss = price + 20
            take_profit = price - 40


        position = Position(
            symbol=symbol,
            side=decision,
            entry_price=price,
            volume=volume,
            stop_loss=stop_loss,
            take_profit=take_profit
        )


        return {
            "status": "OPENED",
            "position": position.to_dict()
        }
