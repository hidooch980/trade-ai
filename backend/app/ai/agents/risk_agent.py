from .base_agent import BaseAgent


class RiskAgent(BaseAgent):

    def __init__(self):
        super().__init__("Risk AI")

    async def analyze(self, market_data):
        return self.result(
            "WAIT",
            90,
            "Risk validation pending"
        )
