class PositionManager:

    def can_open(
        self,
        symbol,
        side,
        positions
    ):

        for pos in positions:

            if (
                pos.get("status","OPEN") == "OPEN"
                and pos.get("symbol") == symbol
                and pos.get("side") == side
            ):
                return {
                    "allowed": False,
                    "reason": "POSITION_ALREADY_OPEN"
                }

        return {
            "allowed": True,
            "reason": "NO_POSITION"
        }


    def create_position(
        self,
        order,
        price
    ):

        return {
            "symbol": order["symbol"],
            "side": order["side"],
            "volume": order["volume"],
            "entry_price": price,
            "stop_loss": price - 10,
            "take_profit": price + 20,
            "status": "OPEN"
        }


position_manager = PositionManager()
