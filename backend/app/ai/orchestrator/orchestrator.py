from app.ai.agents.agent_manager import AgentManager
from app.ai.agents.macro_agent import MacroAgent
from app.ai.agents.news_agent import NewsAgent
from app.ai.agents.smart_money_agent import SmartMoneyAgent
from app.ai.agents.quant_agent import QuantAgent
from app.ai.agents.risk_agent import RiskAgent
from app.ai.committee.investment_committee import InvestmentCommittee
from app.ai.decision.decision_engine import DecisionEngine
from app.ai.risk import RiskGovernor


class AIOrchestrator:

    def __init__(self):

        manager = AgentManager()

        manager.register(MacroAgent())
        manager.register(NewsAgent())
        manager.register(SmartMoneyAgent())
        manager.register(QuantAgent())
        manager.register(RiskAgent())

        committee = InvestmentCommittee(
            manager.agents
        )

        risk = RiskGovernor()

        self.engine = DecisionEngine(
            committee,
            risk
        )

    async def analyze(self, market_data):
        return await self.engine.decide(market_data)
