class GlobalMarketScanner:

    def __init__(self):
        self.markets=[
            "XAUUSD",
            "EURUSD",
            "GBPUSD",
            "BTCUSD",
            "ETHUSD"
        ]


    def scan(self,data):

        results=[]

        for symbol in self.markets:

            market=data.get(symbol,{})

            score=50

            if market.get("trend")=="BULLISH":
                score+=20

            if market.get("volume",0)>0:
                score+=10

            results.append({
                "symbol":symbol,
                "score":score,
                "status":"WATCH"
            })

        return sorted(
            results,
            key=lambda x:x["score"],
            reverse=True
        )


scanner=GlobalMarketScanner()
