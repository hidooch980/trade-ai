from app.execution.trade_history import trade_history
from app.execution.position_store import position_store
from app.ai.learning.trade_learning_engine import trade_learning_engine
from app.ai.learning.trade_result_pipeline import trade_result_pipeline


class CloseManager:

    async def close(
        self,
        mt5,
        ticket,
        exit_price=None,
        reason="EXIT_TRIGGERED"
    ):
        positions = position_store.get_all()

        for pos in positions:

            if pos.get("ticket") != ticket:
                continue

            if pos.get("status") != "OPEN":
                return {
                    "closed": False,
                    "reason": "POSITION_NOT_OPEN",
                    "ticket": ticket
                }

            price = (
                exit_price
                if exit_price is not None
                else pos.get(
                    "current_price",
                    getattr(mt5, "last_price", pos.get("entry_price", 0))
                )
            )

            clean_pos = {
                "ticket": pos.get("ticket"),
                "symbol": pos.get("symbol"),
                "side": pos.get("side"),
                "volume": pos.get("volume"),
                "entry_price": pos.get("entry_price")
            }

            # 1. بستن در لایه MT5 قبل از حذف داخلی
            if hasattr(mt5, "close_position"):
                mt5_result = await mt5.close_position(
                    ticket=ticket,
                    price=price
                )

                if not mt5_result.get("closed"):
                    return {
                        "closed": False,
                        "reason": mt5_result.get(
                            "reason",
                            "MT5_CLOSE_FAILED"
                        ),
                        "ticket": ticket,
                        "mt5": mt5_result
                    }
            else:
                return {
                    "closed": False,
                    "reason": "MT5_CLOSE_METHOD_MISSING",
                    "ticket": ticket
                }

            # 2. ثبت تاریخچه — فقط یک بار
            trade = trade_history.add(
                clean_pos,
                price,
                reason
            )

            # 3. CLOSED position remains in PositionStore as immutable audit record.
            # mt5.close_position() already persisted status, close_price,
            # closed_at and realized pnl.

            # 4. ارسال نتیجه به سیستم یادگیری — فقط یک بار
            learning_result = trade_result_pipeline.process(
                ticket=pos.get("ticket"),
                symbol=pos.get("symbol"),
                decision=pos.get("side"),
                entry_price=pos.get("entry_price"),
                exit_price=price,
                volume=pos.get("volume"),
                pnl=trade.get("pnl", 0),
                strategy="SMART_MONEY_M1"
            )

            # 4. یادگیری مستقیم قدیمی نیز حفظ می‌شود

            return {
                "closed": True,
                "ticket": ticket,
                "symbol": pos.get("symbol"),
                "reason": reason,
                "trade": trade,
                "learning": learning_result
            }

        return {
            "closed": False,
            "reason": "POSITION_NOT_FOUND",
            "ticket": ticket
        }


close_manager = CloseManager()
