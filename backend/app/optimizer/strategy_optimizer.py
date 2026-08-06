from app.backtest.backtest_engine import backtest_engine


class StrategyOptimizer:

    def optimize(
        self,
        symbol,
        candles
    ):

        results = []

        for tp in [10,20,30,50]:

            for sl in [5,10,20]:

                result = backtest_engine.run(
                    symbol,
                    candles,
                    tp,
                    sl
                )

                results.append({
                    "tp": tp,
                    "sl": sl,
                    "profit": result["profit"],
                    "performance": result["performance"]
                })


        best = max(
            results,
            key=lambda x: x["profit"]
        )


        return {
            "best": best,
            "results": results
        }


strategy_optimizer = StrategyOptimizer()
