from typing import List, Dict


class AgentManager:

    def __init__(self):
        self.agents = []

    def register(self, agent):
        self.agents.append(agent)

    async def analyze_all(self, market_data: Dict):
        results = []

        for agent in self.agents:
            result = await agent.analyze(market_data)
            results.append(result)

        return results
