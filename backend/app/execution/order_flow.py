from app.execution.trade_executor import TradeExecutor

class OrderFlow:

    def __init__(self):
        self.executor=TradeExecutor()

    async def process(self,symbol,signal,risk):
        result=await self.executor.execute(
            symbol,
            signal,
            risk
        )
        return result

order_flow=OrderFlow()
