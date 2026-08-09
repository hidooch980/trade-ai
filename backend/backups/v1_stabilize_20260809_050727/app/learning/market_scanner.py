from app.learning.technical_analyzer import technical_analyzer
from app.decision.signal_fusion_engine import signal_fusion_engine


class MarketScanner:

    def scan(self, symbols):

        results = []

        for symbol in symbols:
            try:
                result = signal_fusion_engine.analyze(symbol)

                results.append(result)

            except Exception:
                continue

        results.sort(
            key=lambda x: x.get("confidence",0),
            reverse=True
        )

        return {
            "total": len(results),
            "top": results[:20]
        }


market_scanner = MarketScanner()
