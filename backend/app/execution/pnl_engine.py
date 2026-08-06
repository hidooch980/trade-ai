class PNLEngine:

    def calculate(self, position, current_price):

        if position["side"] == "BUY":
            pnl = (
                current_price - position["entry_price"]
            ) * position["volume"]

        else:
            pnl = (
                position["entry_price"] - current_price
            ) * position["volume"]

        return {
            "symbol": position["symbol"],
            "side": position["side"],
            "entry_price": position["entry_price"],
            "current_price": current_price,
            "volume": position["volume"],
            "pnl": round(pnl, 2),
            "stop_loss": position["stop_loss"],
            "take_profit": position["take_profit"]
        }


pnl_engine = PNLEngine()
