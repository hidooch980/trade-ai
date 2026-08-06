class LiquidityEngine:

    def __init__(self):
        self.market_data=[]


    def analyze(self,symbol,volume,buy_volume,sell_volume):

        imbalance=buy_volume-sell_volume

        pressure="BUY" if imbalance>0 else "SELL"

        liquidity="HIGH"

        if volume<100:
            liquidity="LOW"

        result={
            "symbol":symbol,
            "volume":volume,
            "pressure":pressure,
            "liquidity":liquidity,
            "imbalance":imbalance
        }

        self.market_data.append(result)

        return result


    def smart_money(self,orders):

        large=[]

        for order in orders:
            if order.get("volume",0)>1000:
                large.append(order)

        return {
            "institutional_activity":len(large)>0,
            "large_orders":large
        }


liquidity_engine=LiquidityEngine()
