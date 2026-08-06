from app.ai.agent_weighting import AgentWeightingEngine


reports = [
    {
        "agent": "Quant AI",
        "signal": "BUY"
    },
    {
        "agent": "Smart Money AI",
        "signal": "BUY"
    },
    {
        "agent": "Risk AI",
        "signal": "WAIT"
    },
    {
        "agent": "Macro AI",
        "signal": "BUY"
    },
    {
        "agent": "News AI",
        "signal": "WAIT"
    }
]


result = AgentWeightingEngine().calculate(
    reports
)

print("WEIGHTED AI RESULT:")
print(result)
