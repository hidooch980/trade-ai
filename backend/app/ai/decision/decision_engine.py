from typing import Dict


class DecisionEngine:

    def __init__(self, committee, risk_governor=None):
        self.committee = committee
        self.risk_governor = risk_governor

    async def decide(self, market_data: Dict) -> Dict:

        result = await self.committee.analyze(market_data)

        if self.risk_governor:

            risk_check = self.risk_governor.validate(
                market_data.get("trade", {})
            )

            result["risk"] = risk_check

            if not risk_check["approved"]:
                result["decision"] = "WAIT"
                result["reason"] = "Blocked by Risk Governor"
                return result

        if result["confidence"] < 70:
            result["decision"] = "WAIT"
            result["reason"] = "Confidence below safety threshold"
        else:
            result["reason"] = "Committee consensus approved"

        return result
