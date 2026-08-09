from app.broker.core.router import broker_router
from app.broker.discovery.broker_detector import broker_detector


class BrokerSearch:
    async def search(self, query: str) -> dict:
        query = str(query or "").strip()

        adapter = broker_router.resolve(query)
        detection = broker_detector.detect(query)

        return {
            "query": query,
            "registered": adapter is not None,
            "adapter": adapter.__name__ if adapter else None,
            "detection": detection,
            "brokers": broker_router.available(),
            "requires_external_discovery": adapter is None,
        }


broker_search = BrokerSearch()
