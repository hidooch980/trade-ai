from app.optimizer.strategy_optimizer import strategy_optimizer
from app.ai.memory.strategy_memory import strategy_memory


class OptimizerService:


    def optimize_and_save(
        self,
        symbol,
        timeframe,
        candles
    ):

        result = strategy_optimizer.optimize(
            symbol,
            candles
        )


        best = result["best"]


        strategy_memory.save(
            symbol,
            timeframe,
            {
                "tp": best["tp"],
                "sl": best["sl"],
                "profit": best["profit"],
                "performance": best["performance"]
            }
        )


        return strategy_memory.get(
            symbol,
            timeframe
        )


optimizer_service = OptimizerService()
