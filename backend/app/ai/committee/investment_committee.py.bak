from typing import List, Dict


class InvestmentCommittee:

    def __init__(self, agents: List):
        self.agents = agents

    async def analyze(self, market_data: Dict) -> Dict:
        reports = []

        for agent in self.agents:
            result = await agent.analyze(market_data)
            reports.append(result)

        return self.vote(reports)

    def vote(self, reports: List[Dict]) -> Dict:
        buy = 0
        sell = 0
        wait = 0
        confidence = 0

        for report in reports:
            signal = report.get("signal")

            if signal == "BUY":
                buy += 1
            elif signal == "SELL":
                sell += 1
            else:
                wait += 1

            confidence += report.get("confidence", 0)

        total = len(reports) or 1

        if buy > sell and buy > wait:
            decision = "BUY"
        elif sell > buy and sell > wait:
            decision = "SELL"
        else:
            decision = "WAIT"

        return {
            "decision": decision,
            "confidence": round(confidence / total, 2),
            "votes": {
                "BUY": buy,
                "SELL": sell,
                "WAIT": wait
            },
            "reports": reports
        }
