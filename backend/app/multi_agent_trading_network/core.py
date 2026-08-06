class AIMultiAgentTradingNetwork:

    def __init__(self):
        self.agents=[]
        self.messages=[]
        self.decisions=[]
        self.performance=[]


    def register_agent(self,name,role):

        agent={
            "name":name,
            "role":role,
            "status":"ACTIVE"
        }

        self.agents.append(agent)

        return agent


    def send_message(self,message):

        self.messages.append(message)


    def create_consensus(self,opinions):

        decision={
            "opinions":opinions,
            "result":"CONSENSUS"
        }

        self.decisions.append(decision)

        return decision


    def record_performance(self,data):

        self.performance.append(data)


    def status(self):

        return {
            "agents":len(self.agents),
            "messages":len(self.messages),
            "decisions":len(self.decisions),
            "performance":len(self.performance),
            "network":"ONLINE"
        }


multi_agent_network=AIMultiAgentTradingNetwork()
