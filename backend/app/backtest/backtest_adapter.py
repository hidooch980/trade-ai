class BacktestAdapter:

    def __init__(self, decision_engine=None):
        self.decision_engine = decision_engine

    async def run(self, candles):

        trades = []

        for candle in candles:

            if self.decision_engine:
                decision = await self.decision_engine.decide(
                    candle.model_dump()
                )
            else:
                decision = {
                    "decision": "WAIT"
                }

            trades.append({
                "symbol": candle.symbol,
                "timeframe": candle.timeframe,
                "close": candle.close,
                "decision": decision
            })

        return {
            "total_candles": len(candles),
            "trades": trades
        }
