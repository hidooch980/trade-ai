class GlobalIntelligenceNetwork:

    def __init__(self):
        self.agents={}
        self.knowledge=[]


    def register_agent(self,name):

        self.agents[name]={
            "score":50,
            "status":"ACTIVE"
        }

        return self.agents[name]


    def share_knowledge(self,data):

        self.knowledge.append(data)

        return {
            "stored":True,
            "knowledge_size":len(self.knowledge)
        }


    def update_agent(self,name,result):

        agent=self.agents.get(name)

        if agent:

            if result=="GOOD":
                agent["score"]=min(
                    agent["score"]+5,
                    100
                )

            else:
                agent["score"]=max(
                    agent["score"]-5,
                    0
                )

        return agent


    def status(self):

        return {
            "agents":len(self.agents),
            "knowledge":len(self.knowledge),
            "network":"ONLINE"
        }


global_intelligence=GlobalIntelligenceNetwork()
