class IndicatorAIBridge:

    def __init__(self, ai_orchestrator):
        self.ai_orchestrator = ai_orchestrator


    async def analyze_with_indicators(
        self,
        market_data,
        indicators
    ):

        context = {
            "market": market_data,
            "indicators": indicators
        }

        decision = await self.ai_orchestrator.analyze(
            context
        )

        return {
            "context": context,
            "decision": decision
        }
