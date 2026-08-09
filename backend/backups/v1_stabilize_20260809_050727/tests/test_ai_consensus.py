from app.ai.consensus.consensus_engine import AIConsensusEngine


reports = [

    {
        "agent": "Macro AI",
        "signal": "BUY",
        "confidence": 80
    },

    {
        "agent": "News AI",
        "signal": "BUY",
        "confidence": 70
    },

    {
        "agent": "Quant AI",
        "signal": "WAIT",
        "confidence": 60
    },

    {
        "agent": "Risk AI",
        "signal": "BUY",
        "confidence": 90
    },

    {
        "agent": "Smart Money AI",
        "signal": "BUY",
        "confidence": 85
    }

]


result = AIConsensusEngine().analyze(
    reports
)


print("AI CONSENSUS RESULT:")
print(result)
