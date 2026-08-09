from .base_agent import BaseAgent
from app.market.macro import MacroEngine


class MacroAgent(BaseAgent):

    def __init__(self):
        super().__init__("Macro AI")
        self.engine = MacroEngine()


    async def analyze(self, market_data):

        macro_data = market_data.get(
            "macro",
            {}
        )

        result = self.engine.analyze(
            macro_data
        )

        score = result["macro_score"]

        signal = "WAIT"
        confidence = 60

        if score >= 60:
            signal = "BUY"
            confidence = 70

        elif score <= 40:
            signal = "SELL"
            confidence = 70


        return self.result(
            signal,
            confidence,
            result
        )
