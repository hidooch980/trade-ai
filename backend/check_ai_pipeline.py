from app.decision.final_decision_engine import FinalDecisionEngine
from app.learning.market_memory import market_memory
from app.ai.memory.adaptive_strategy_memory import adaptive_strategy_memory
from app.learning.reward_engine import reward_engine
from app.execution.position_store import position_store
from app.execution.trade_history import trade_history


print("===== FINAL DECISION TEST =====")

engine = FinalDecisionEngine()

result = engine.decide(
    {
        "trend": "BULLISH",
        "score": 50
    },
    {
        "decision": "BUY"
    },
    {
        "approved": True,
        "volume": 1
    },
    {
        "score": 50
    }
)

print(result)


print("\n===== MARKET MEMORY =====")
print(market_memory.status())


print("\n===== ADAPTIVE MEMORY =====")
print(
    adaptive_strategy_memory.get_weight(
        "SMART_MONEY_M1"
    )
)


print("\n===== REWARD MEMORY =====")
print(
    reward_engine.get_score("BUY")
)


print("\n===== OPEN POSITIONS =====")
print(
    position_store.get_all()
)


print("\n===== CLOSED TRADES =====")
print(
    len(trade_history.closed_trades)
)


print("\n===== AI PIPELINE STATUS: ONLINE =====")
