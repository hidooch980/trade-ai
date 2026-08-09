from typing import List, Dict
from app.ai.agent_weighting import AgentWeightingEngine


class InvestmentCommittee:

    def __init__(self, agents: List):
        self.agents = agents
        self.weighting = AgentWeightingEngine()

    async def analyze(self, market_data: Dict) -> Dict:
        reports = []

        for agent in self.agents:
            result = await agent.analyze(market_data)
            reports.append(result)

        return self.vote(reports)

    def vote(self, reports: List[Dict]) -> Dict:
        weighted = self.weighting.calculate(reports)

        return {
            "decision": weighted["decision"],
            "confidence": weighted["confidence"],
            "weighted_scores": weighted["weighted_scores"],
            "reports": reports
        }
