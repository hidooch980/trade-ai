class TradingAgent:

    def __init__(self,name,role):
        self.name=name
        self.role=role
        self.status="ACTIVE"


    def analyze(self,data):

        return {
            "agent":self.name,
            "role":self.role,
            "result":"ANALYZED"
        }


class AgentWorkforce:

    def __init__(self):
        self.agents={}


    def create_agent(self,name,role):

        agent=TradingAgent(name,role)

        self.agents[name]=agent

        return {
            "name":name,
            "role":role,
            "status":"CREATED"
        }


    def run_all(self,data):

        results=[]

        for agent in self.agents.values():
            results.append(agent.analyze(data))

        return results


    def status(self):

        return {
            "agents":len(self.agents),
            "workforce":"ONLINE"
        }


agent_workforce=AgentWorkforce()
