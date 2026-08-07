from app.execution.trade_history import trade_history
from app.execution.position_store import position_store
from app.ai.learning.trade_learning_engine import trade_learning_engine

class CloseManager:
    async def close(self, mt5, ticket, exit_price=None):
        positions = position_store.get_all()

        for pos in positions:
            if pos.get("ticket") == ticket:

                price = exit_price if exit_price is not None else pos.get("current_price", mt5.last_price)

                clean_pos = {
                    "ticket": pos.get("ticket"),
                    "symbol": pos.get("symbol"),
                    "side": pos.get("side"),
                    "volume": pos.get("volume"),
                    "entry_price": pos.get("entry_price")
                }

                trade = trade_history.add(
                    clean_pos,
                    price,
                    "EXIT_TRIGGERED"
                )

                trade_learning_engine.record_trade(
                    trade
                )

                position_store.remove(ticket)

                return {
                    "trade": trade,
                    "closed": True,
                    "ticket": ticket,
                    "symbol": pos.get("symbol"),
                    "reason": "EXIT_TRIGGERED"
                }

        return {
            "closed": False,
            "reason": "POSITION_NOT_FOUND"
        }

close_manager=CloseManager()
