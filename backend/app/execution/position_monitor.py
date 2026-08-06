from app.execution.break_even import break_even
from app.execution.trailing_stop import trailing_stop
from app.execution.position_store import position_store
from app.execution.trade_history import trade_history

class PositionMonitor:

    def check(self, positions, price):
        actions=[]

        for p in positions:
            current = price

            if p.get("side") == "BUY":
                pnl = (current - p.get("entry_price",0)) * p.get("volume",0)
            else:
                pnl = (p.get("entry_price",0) - current) * p.get("volume",0)

            if p.get("take_profit") and current >= p["take_profit"]:
                actions.append({
                    "ticket": p["ticket"],
                    "action": "CLOSE",
                    "reason": "TAKE_PROFIT",
                    "pnl": pnl
                })

            if p.get("stop_loss") and current <= p["stop_loss"]:
                actions.append({
                    "ticket": p["ticket"],
                    "action": "CLOSE",
                    "reason": "STOP_LOSS",
                    "pnl": pnl
                })

        return actions

    def update(self, price):
        closed=[]
        for p in position_store.get_all()[:]:
            p["current_price"]=price
            trailing_stop.update(p)
            break_even.update(p)
            if p["side"]=="BUY":
                p["pnl"]=(price-p["entry_price"])*p["volume"]
                if p.get("take_profit") and price>=p["take_profit"]:
                    closed.append(p)
                if p.get("stop_loss") and price<=p["stop_loss"]:
                    closed.append(p)
            else:
                p["pnl"]=(p["entry_price"]-price)*p["volume"]
        for p in closed:
            position_store.remove(p["ticket"])
            trade_history.closed_trades.append({
                **p,
                "close_price":p["current_price"],
                "reason":"SL_TP_TRIGGERED"
            })
        return position_store.get_all()

position_monitor=PositionMonitor()
