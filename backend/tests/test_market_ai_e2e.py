import asyncio

from app.market_data.providers.mock_provider import MockMarketDataProvider
from app.market_data.services.data_service import MarketDataService
from app.integration.market_ai_bridge import MarketAIBridge
from app.ai.orchestrator import AIOrchestrator


async def main():

    provider = MockMarketDataProvider()

    market_service = MarketDataService(
        provider=provider
    )

    ai_system = AIOrchestrator()

    bridge = MarketAIBridge(
        market_service,
        ai_system
    )

    result = await bridge.analyze_symbol(
        "XAUUSD",
        "H1"
    )

    print("END TO END RESULT:")
    print(result)


asyncio.run(main())
