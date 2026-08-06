class AgentMarketplace:

    def __init__(self):
        self.agents={}
        self.subscriptions=[]


    def register(self,name,owner,category):

        self.agents[name]={
            "owner":owner,
            "category":category,
            "score":50,
            "status":"ACTIVE"
        }

        return self.agents[name]


    def evaluate(self,name,score):

        agent=self.agents.get(name)

        if agent:
            agent["score"]=score

        return agent


    def subscribe(self,user,agent):

        if agent in self.agents:

            self.subscriptions.append({
                "user":user,
                "agent":agent
            })

            return {
                "status":"SUBSCRIBED"
            }

        return None


    def status(self):

        return {
            "agents":len(self.agents),
            "subscriptions":len(self.subscriptions)
        }


agent_marketplace=AgentMarketplace()
