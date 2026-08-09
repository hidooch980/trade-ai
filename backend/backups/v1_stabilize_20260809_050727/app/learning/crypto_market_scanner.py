from app.learning.crypto_universe import crypto_universe
from app.decision.signal_fusion_engine import signal_fusion_engine


class CryptoMarketScanner:

    def scan_top200(self):

        coins = crypto_universe.get_top200()

        results = []

        for coin in coins:

            symbol = coin["symbol"]

            try:
                analysis = signal_fusion_engine.analyze(symbol)

                results.append({
                    "symbol": symbol,
                    "decision": analysis.get("decision"),
                    "score": analysis.get("score"),
                    "confidence": analysis.get("confidence"),
                    "reasons": analysis.get("reasons")
                })

            except Exception:
                continue


        results.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )


        return {
            "scanned": len(results),
            "top_buy": [
                x for x in results
                if x["decision"] == "BUY"
            ][:20],

            "top_sell": [
                x for x in results
                if x["decision"] == "SELL"
            ][:20],

            "watch": [
                x for x in results
                if x["decision"] == "HOLD"
            ][:20]
        }


crypto_market_scanner = CryptoMarketScanner()
