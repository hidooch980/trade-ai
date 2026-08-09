import json
from datetime import datetime
from pathlib import Path


HISTORY_FILE = Path("/opt/trade-ai/backend/closed_trades.json")


class TradeHistory:

    def __init__(self):
        self.closed_trades = []
        self.load()


    def load(self):
        if HISTORY_FILE.exists():
            try:
                self.closed_trades = json.loads(
                    HISTORY_FILE.read_text()
                )
            except:
                self.closed_trades = []


    def save(self):
        HISTORY_FILE.write_text(
            json.dumps(
                self.closed_trades,
                indent=2
            )
        )


    def add(
        self,
        position,
        close_price,
        reason
    ):

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
        self.save()

        return trade


trade_history = TradeHistory()
