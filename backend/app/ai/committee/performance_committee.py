from app.performance import WinRateEngine


class PerformanceCommittee:


    def __init__(self, agents):

        self.agents = agents
        self.win_engine = WinRateEngine()



    async def vote(self, market_data):

        results = []

        for agent in self.agents:

            result = await agent.analyze(
                market_data
            )

            history = result.get(
                "history",
                []
            )

            performance = self.win_engine.calculate(
                history
            )

            weight = self.win_engine.agent_score(
                performance["win_rate"]
            )

            result["weight"] = weight
            result["win_rate"] = performance["win_rate"]

            results.append(result)


        return results
