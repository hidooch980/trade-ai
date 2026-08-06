from app.ai.learning.feedback_loop import feedback_loop
from app.optimizer.optimizer_service import optimizer_service


class AutoOptimizer:


    def check_and_optimize(
        self,
        symbol,
        timeframe,
        candles
    ):

        feedback = feedback_loop.analyze(
            symbol,
            timeframe
        )


        if feedback.get("status") == "NO_DATA":
            return {
                "status":"NO_DATA"
            }


        win_rate = feedback.get(
            "win_rate",
            0
        )


        if win_rate < 60:

            result = optimizer_service.optimize_and_save(
                symbol,
                timeframe,
                candles
            )

            return {
                "status":"REOPTIMIZED",
                "feedback":feedback,
                "new_strategy":result
            }


        return {
            "status":"STRATEGY_OK",
            "feedback":feedback
        }


auto_optimizer = AutoOptimizer()
