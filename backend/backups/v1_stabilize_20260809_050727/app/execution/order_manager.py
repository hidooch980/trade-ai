from app.execution.trade_executor import TradeExecutor


class OrderManager:

    def __init__(self):
        self.executor = TradeExecutor()

    async def open(self, symbol, signal, risk):
        return await self.executor.execute(
            symbol,
            signal,
            risk
        )

    async def close(
        self,
        mt5,
        ticket,
        exit_price=None,
        reason="MANUAL_CLOSE"
    ):
        from app.execution.close_manager import close_manager

        return await close_manager.close(
            mt5,
            ticket,
            exit_price=exit_price,
            reason=reason
        )


order_manager = OrderManager()
