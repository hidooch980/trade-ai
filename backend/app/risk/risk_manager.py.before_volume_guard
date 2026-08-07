class RiskManager:

    def __init__(self):
        self.daily_loss_limit = 500
        self.max_exposure = 100000

    def check(self, positions, volume, price):
        exposure = sum(
            p.get("volume",0) * p.get("entry_price",0)
            for p in positions
        )

        if exposure + (volume * price) > self.max_exposure:
            return {
                "approved":False,
                "reason":"MAX_EXPOSURE_LIMIT"
            }

        loss = sum(
            p.get("pnl",0)
            for p in positions
            if p.get("pnl",0) < 0
        )

        if abs(loss) >= self.daily_loss_limit:
            return {
                "approved":False,
                "reason":"DAILY_LOSS_LIMIT"
            }

        return {
            "approved":True,
            "reason":"RISK_OK"
        }


risk_manager = RiskManager()
