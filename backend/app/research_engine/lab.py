class AIResearchEngine:

    def __init__(self):
        self.experiments=[]
        self.discoveries=[]
        self.proposals=[]


    def create_experiment(self,name,data):

        experiment={
            "name":name,
            "data":data,
            "status":"RUNNING"
        }

        self.experiments.append(experiment)

        return experiment


    def add_discovery(self,pattern):

        item={
            "pattern":pattern,
            "status":"DISCOVERED"
        }

        self.discoveries.append(item)

        return item


    def create_proposal(self,idea):

        proposal={
            "idea":idea,
            "status":"WAITING_APPROVAL"
        }

        self.proposals.append(proposal)

        return proposal


    def status(self):

        return {
            "experiments":len(self.experiments),
            "discoveries":len(self.discoveries),
            "proposals":len(self.proposals),
            "research":"ONLINE"
        }


research_engine=AIResearchEngine()
