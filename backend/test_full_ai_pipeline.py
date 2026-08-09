from app.decision.final_decision_engine import FinalDecisionEngine
from app.execution.order_flow import order_flow


engine = FinalDecisionEngine()


def test_buy():

    decision = engine.decide(
        {
            "trend": "BULLISH",
            "score": 60
        },
        {
            "decision": "BUY"
        },
        {
            "approved": True,
            "volume": 1,
            "entry_price": 1.1000,
            "stop_loss": 1.0900,
            "take_profit": 1.1200
        },
        {
            "score": 70
        }
    )

    print("\n===== AI DECISION BUY =====")
    print(decision)

    return decision


def test_sell():

    decision = engine.decide(
        {
            "trend": "BEARISH",
            "score": -60
        },
        {
            "decision": "SELL"
        },
        {
            "approved": True,
            "volume": 1,
            "entry_price": 1.1000,
            "stop_loss": 1.1100,
            "take_profit": 1.0800
        },
        {
            "score": -70
        }
    )

    print("\n===== AI DECISION SELL =====")
    print(decision)

    return decision


if __name__ == "__main__":

    buy = test_buy()
    sell = test_sell()

    print("\n===== PIPELINE STATUS =====")
    print("DECISION ENGINE ONLINE")
