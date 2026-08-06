class AIMultiAgentSystem:

    def __init__(self):
        self.agents={}
        self.decisions=[]
        self.memory=[]


    def register_agent(self,name,role):

        self.agents[name]={
            "role":role,
            "status":"ACTIVE"
        }

        return self.agents[name]


    def submit_analysis(self,agent,result):

        decision={
            "agent":agent,
            "result":result
        }

        self.decisions.append(decision)

        return decision


    def store_memory(self,data):

        self.memory.append(data)

        return {
            "status":"STORED"
        }


    def generate_decision(self):

        return {
            "agents":len(self.agents),
            "decision":"GENERATED"
        }


    def status(self):

        return {
            "agents":len(self.agents),
            "decisions":len(self.decisions),
            "memory":len(self.memory),
            "system":"ONLINE"
        }


multi_agent_system=AIMultiAgentSystem()
