import time


class AIControlCenter:

    def __init__(self):
        self.system="TRADE_AI"

    def overview(self):
        return {
            "system":self.system,
            "status":"ONLINE",
            "ai":"ACTIVE",
            "market_engine":"RUNNING",
            "risk_engine":"ACTIVE",
            "broker_gateway":"READY",
            "timestamp":time.time()
        }


    def performance(self,trades):

        total=len(trades)
        profit=sum(
            t.get("pnl",0)
            for t in trades
        )

        return {
            "total_trades":total,
            "profit":profit
        }


control_center=AIControlCenter()
