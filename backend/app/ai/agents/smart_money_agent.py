from .base_agent import BaseAgent
from app.market.smart_money import SmartMoneyEngine


class SmartMoneyAgent(BaseAgent):

    def __init__(self):
        super().__init__("Smart Money AI")
        self.engine = SmartMoneyEngine()


    async def analyze(self, market_data):

        prices = market_data.get("prices", [])

        if len(prices) < 10:
            return self.result(
                "WAIT",
                50,
                "Not enough liquidity data"
            )

        structure = self.engine.detect_structure(prices)
        liquidity = self.engine.liquidity_zone(prices)

        signal = "WAIT"
        confidence = 65

        if structure["trend"] == "BULLISH":
            signal = "BUY"
            confidence = 75

        elif structure["trend"] == "BEARISH":
            signal = "SELL"
            confidence = 75


        return self.result(
            signal,
            confidence,
            {
                "structure": structure,
                "liquidity": liquidity
            }
        )
