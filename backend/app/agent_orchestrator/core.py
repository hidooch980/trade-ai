class AIAgentOrchestrator:

    def __init__(self):
        self.agents=[]
        self.tasks=[]
        self.messages=[]
        self.decisions=[]


    def register_agent(self,name,role):

        agent={
            "name":name,
            "role":role,
            "status":"ACTIVE"
        }

        self.agents.append(agent)

        return agent


    def create_task(self,task,agent):

        item={
            "task":task,
            "agent":agent,
            "status":"ASSIGNED"
        }

        self.tasks.append(item)

        return item


    def send_message(self,source,target,message):

        item={
            "source":source,
            "target":target,
            "message":message
        }

        self.messages.append(item)

        return item


    def aggregate_decision(self,data):

        decision={
            "input":data,
            "status":"GENERATED"
        }

        self.decisions.append(decision)

        return decision


    def status(self):

        return {
            "agents":len(self.agents),
            "tasks":len(self.tasks),
            "messages":len(self.messages),
            "decisions":len(self.decisions),
            "orchestrator":"ONLINE"
        }


agent_orchestrator=AIAgentOrchestrator()
