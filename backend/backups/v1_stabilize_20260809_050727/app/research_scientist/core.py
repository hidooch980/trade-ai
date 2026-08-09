class AIMarketResearchScientist:

    def __init__(self):
        self.observations=[]
        self.hypotheses=[]
        self.experiments=[]
        self.knowledge=[]


    def observe(self,data):

        item={
            "data":data,
            "status":"OBSERVED"
        }

        self.observations.append(item)

        return item


    def create_hypothesis(self,idea):

        item={
            "idea":idea,
            "status":"CREATED"
        }

        self.hypotheses.append(item)

        return item


    def run_experiment(self,hypothesis,result):

        item={
            "hypothesis":hypothesis,
            "result":result
        }

        self.experiments.append(item)

        return item


    def extract_knowledge(self,finding):

        self.knowledge.append(finding)

        return {
            "status":"STORED"
        }


    def status(self):

        return {
            "observations":len(self.observations),
            "hypotheses":len(self.hypotheses),
            "experiments":len(self.experiments),
            "knowledge":len(self.knowledge),
            "scientist":"ONLINE"
        }


research_scientist=AIMarketResearchScientist()
