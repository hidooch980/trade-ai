from typing import Dict


class RiskGovernor:

    def __init__(
        self,
        max_risk_percent: float = 1.0,
        max_daily_drawdown: float = 3.0
    ):
        self.max_risk_percent = max_risk_percent
        self.max_daily_drawdown = max_daily_drawdown

    def validate(self, trade: Dict) -> Dict:

        risk = trade.get("risk_percent", 0)
        drawdown = trade.get("daily_drawdown", 0)

        approved = True
        reasons = []

        if risk > self.max_risk_percent:
            approved = False
            reasons.append("Risk exceeds maximum limit")

        if drawdown > self.max_daily_drawdown:
            approved = False
            reasons.append("Daily drawdown protection activated")

        return {
            "approved": approved,
            "risk_status": "SAFE" if approved else "BLOCKED",
            "reasons": reasons
        }
