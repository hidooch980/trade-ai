from .base_agent import BaseAgent
from app.market.news import NewsEngine


class NewsAgent(BaseAgent):

    def __init__(self):
        super().__init__("News AI")
        self.engine = NewsEngine()


    async def analyze(self, market_data):

        news_data = market_data.get(
            "news",
            []
        )

        result = self.engine.analyze(
            news_data
        )

        score = result["score"]

        signal = "WAIT"
        confidence = 60

        if result["risk"] == "HIGH":
            return self.result(
                "WAIT",
                85,
                {
                    "reason": "High impact news risk",
                    **result
                }
            )

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
