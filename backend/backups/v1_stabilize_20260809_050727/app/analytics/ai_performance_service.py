from app.ai.learning.feedback_loop import feedback_loop
from app.learning.reward_engine import reward_engine
from app.ai.memory.adaptive_strategy_memory import adaptive_strategy_memory


class AIPerformanceService:

    def report(self, symbol, timeframe):

        feedback = feedback_loop.analyze(
            symbol,
            timeframe
        )

        reward_score = reward_engine.get_score(
            "BUY"
        )

        memory = adaptive_strategy_memory.get_weight(
            "SMART_MONEY_M1"
        )

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "feedback": feedback,
            "reward_score": reward_score,
            "strategy_memory": memory,
            "ai_status": "LEARNING"
        }


ai_performance_service = AIPerformanceService()
