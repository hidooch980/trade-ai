from app.decision.final_decision_engine import FinalDecisionEngine


indicator = {
    "decision": "BUY"
}


ai_signal = {
    "decision": "BUY"
}


risk = {
    "approved": True
}


smart_money = {
    "decision": "BUY"
}


result = FinalDecisionEngine().decide(
    indicator,
    ai_signal,
    risk,
    smart_money
)


print("FINAL DECISION:")
print(result)
