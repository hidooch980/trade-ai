from app.market import MarketDataEngine


class MarketAIConnector:


    def __init__(self, orchestrator):

        self.orchestrator = orchestrator
        self.market = MarketDataEngine()



    async def analyze_market(self, candle):

        self.market.add_candle(
            candle
        )

        status = self.market.validate()


        if not status["ready"]:

            return {

                "status": "WAIT",

                "reason":
                    "Not enough market data",

                "candles":
                    status["candles"]

            }


        return await self.orchestrator.analyze(
            self.market.latest()
        )
