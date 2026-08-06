from datetime import datetime


class TradeHistory:

    def __init__(self):
        self.closed_trades = []


    def add(
        self,
        position,
        close_price,
        reason
    ):

        pnl = 0

        if position["side"] == "BUY":
            pnl = (
                close_price -
                position["entry_price"]
            ) * position["volume"]

        else:
            pnl = (
                position["entry_price"] -
                close_price
            ) * position["volume"]


        trade = {
            "ticket": position.get("ticket"),
            "symbol": position["symbol"],
            "side": position["side"],
            "volume": position["volume"],
            "entry_price": position["entry_price"],
            "close_price": close_price,
            "pnl": round(pnl, 2),
            "reason": reason,
            "close_time": datetime.utcnow().isoformat()
        }


        self.closed_trades.append(trade)

        return trade


trade_history = TradeHistory()
