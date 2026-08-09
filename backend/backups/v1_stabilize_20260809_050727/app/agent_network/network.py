class AIAgentNetwork:

    def __init__(self):
        self.agents={}
        self.messages=[]


    def register_agent(self,name,role):

        self.agents[name]={
            "role":role,
            "status":"ONLINE"
        }

        return self.agents[name]


    def send_message(self,source,target,message):

        item={
            "from":source,
            "to":target,
            "message":message
        }

        self.messages.append(item)

        return item


    def coordinate(self,task):

        return {
            "task":task,
            "status":"DISTRIBUTED"
        }


    def status(self):

        return {
            "agents":len(self.agents),
            "messages":len(self.messages),
            "network":"ONLINE"
        }


agent_network=AIAgentNetwork()
