from app.integration.ai.ai_decision_bridge import AIDecisionBridge


consensus = {

    "engine": "AI_CONSENSUS",

    "decision": "BUY",

    "confidence": 77,

    "votes": {
        "BUY": 4,
        "SELL": 0,
        "WAIT": 1
    }
}


final_signal = {

    "decision": "BUY",

    "confidence": 70

}


result = AIDecisionBridge().combine(
    consensus,
    final_signal
)


print("AI ENHANCED FINAL SIGNAL:")
print(result)
