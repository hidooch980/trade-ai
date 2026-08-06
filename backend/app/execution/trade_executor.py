from app.market.bridge.mt5_bridge import mt5_bridge
from app.execution.position_manager import position_manager
from app.execution.position_store import position_store
from app.risk.risk_manager import risk_manager
from app.journal.trade_journal import trade_journal


class TradeExecutor:

    def __init__(self):
        self.mt5 = mt5_bridge


    async def execute(
        self,
        symbol,
        signal,
        risk
    ):

        if signal.get("decision") not in [
            "BUY",
            "SELL"
        ]:
            return {
                "executed": False,
                "reason": "NO_TRADE_SIGNAL"
            }


        if not risk.get("approved"):
            return {
                "executed": False,
                "reason": "RISK_REJECTED"
            }

        risk_check = risk_manager.check(
            position_store.get_all(),
            risk["volume"],
            risk.get("entry_price",0)
        )

        if not risk_check["approved"]:
            return {
                "executed": False,
                "reason": risk_check["reason"]
            }


        account_positions = position_store.get_all()


        position_check = position_manager.can_open(
            symbol,
            signal["decision"],
            account_positions
        )


        if not position_check["allowed"]:
            return {
                "executed": False,
                "reason": position_check["reason"]
            }


        order = {
            "symbol": symbol,
            "side": signal["decision"],
            "volume": risk["volume"],
            "price": risk.get("entry_price", 0)
        }


        mt5_result = await self.mt5.send_order(order)

        trade_journal.add('OPEN_ORDER',order)

        position_store.add({"ticket": mt5_result.get("ticket","SIM-1"),"symbol": symbol,"side": signal["decision"],"volume": risk["volume"],"entry_price": order["price"],"current_price": order["price"],"pnl":0.0,"stop_loss":risk.get("stop_loss",order["price"]-10),"take_profit":risk.get("take_profit",order["price"]+20),"status":"OPEN"})


        return {
            "executed": True,
            "order": {
                **order,
                "status": "PENDING_MT5",
                "mt5": mt5_result
            }
        }
