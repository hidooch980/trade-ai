class AgentWorkforce:

    def __init__(self):
        self.agents={}
        self.tasks=[]


    def register_agent(self,name,role):

        self.agents[name]={
            "role":role,
            "score":50,
            "status":"ACTIVE"
        }

        return self.agents[name]


    def assign_task(self,agent,task):

        if agent in self.agents:

            item={
                "agent":agent,
                "task":task,
                "status":"ASSIGNED"
            }

            self.tasks.append(item)

            return item

        return None


    def evaluate(self,agent,score):

        if agent in self.agents:
            self.agents[agent]["score"]=score

        return self.agents.get(agent)


    def status(self):

        return {
            "agents":len(self.agents),
            "tasks":len(self.tasks),
            "system":"ACTIVE"
        }


agent_workforce=AgentWorkforce()
