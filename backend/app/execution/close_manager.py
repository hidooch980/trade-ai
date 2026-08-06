from app.execution.trade_history import trade_history
from app.execution.position_store import position_store


class CloseManager:

    async def close(self, mt5, ticket):

        positions = await mt5.get_positions()

        for pos in positions:

            if pos.get("ticket") == ticket:

                pos["status"] = "CLOSED"

                trade = trade_history.add(
                    pos,
                    mt5.last_price,
                    "EXIT_TRIGGERED"
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


close_manager = CloseManager()
