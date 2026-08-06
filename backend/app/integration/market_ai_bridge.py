from app.market_data.services.data_service import MarketDataService
from app.ai.orchestrator import AIOrchestrator


class MarketAIBridge:

    def __init__(self, market_service, ai_system):
        self.market_service = market_service
        self.ai_system = ai_system


    async def analyze_symbol(self, symbol, timeframe):

        market = await self.market_service.get_market_candles(
            symbol,
            timeframe,
            limit=1
        )

        if market["count"] == 0:
            return {
                "status": "NO_DATA"
            }

        candle = market["candles"][0]

        decision = await self.ai_system.analyze(
            candle
        )

        return {
            "market": candle,
            "decision": decision
        }
