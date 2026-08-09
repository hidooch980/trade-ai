class AIMultiAgentNetwork:

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


    def send_message(self,source,target,message):

        item={
            "source":source,
            "target":target,
            "message":message
        }

        self.messages.append(item)

        return item


    def create_consensus(self,data):

        decision={
            "input":data,
            "status":"CONSENSUS_READY"
        }

        self.decisions.append(decision)

        return decision


    def record_performance(self,agent,result):

        item={
            "agent":agent,
            "result":result
        }

        self.performance.append(item)

        return item


    def status(self):

        return {
            "agents":len(self.agents),
            "messages":len(self.messages),
            "decisions":len(self.decisions),
            "performance":len(self.performance),
            "network":"ONLINE"
        }


multi_agent_network=AIMultiAgentNetwork()
