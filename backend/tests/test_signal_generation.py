from app.signals.services.signal_generator import SignalGenerator


ai_result = {
    "decision": "BUY",
    "confidence": 78,
    "weighted_scores": {
        "BUY": 0.65,
        "SELL": 0.15,
        "WAIT": 0.20
    }
}


risk_result = {
    "approved": True,
    "final_decision": "BUY",
    "checks": {
        "win_rate": True,
        "risk_reward": True,
        "volatility": True
    }
}


signal = SignalGenerator().generate(
    symbol="XAUUSD",
    decision_result=ai_result,
    risk_result=risk_result
)


print("FINAL SIGNAL:")
print(signal.to_dict())
