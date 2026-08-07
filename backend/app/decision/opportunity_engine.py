class OpportunityEngine:


    def rank(self, scan_result):

        opportunities = []

        for item in scan_result.get("top_buy", []):

            opportunities.append({
                "symbol": item["symbol"],
                "side": "BUY",
                "score": item["score"],
                "confidence": item["confidence"],
                "reasons": item["reasons"]
            })


        for item in scan_result.get("top_sell", []):

            opportunities.append({
                "symbol": item["symbol"],
                "side": "SELL",
                "score": item["score"],
                "confidence": item["confidence"],
                "reasons": item["reasons"]
            })


        opportunities.sort(
            key=lambda x: abs(x["score"]),
            reverse=True
        )


        return {
            "count": len(opportunities),
            "best": opportunities[:10]
        }



opportunity_engine = OpportunityEngine()
