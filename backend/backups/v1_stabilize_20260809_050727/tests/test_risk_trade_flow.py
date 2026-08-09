from app.integration.risk.risk_decision_bridge import RiskDecisionBridge


decision = {
    "engine": "FINAL_DECISION",
    "decision": "BUY",
    "score": 100
}


risk_result = {
    "approved": True,
    "risk_amount": 200,
    "volume": 10
}


result = RiskDecisionBridge().validate(
    decision,
    risk_result
)


print("RISK TRADE FLOW:")
print(result)
