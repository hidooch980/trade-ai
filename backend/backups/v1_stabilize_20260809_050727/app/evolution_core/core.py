class AIEvolutionCore:

    def __init__(self):
        self.models={}
        self.history=[]


    def register_model(self,name,score=50):

        self.models[name]={
            "score":score,
            "version":1
        }

        return self.models[name]


    def learn(self,data):

        self.history.append(data)

        return {
            "learning":True,
            "samples":len(self.history)
        }


    def evolve(self,name,result):

        model=self.models.get(name)

        if not model:
            return None

        if result=="BETTER":
            model["score"]=min(
                model["score"]+10,
                100
            )
            model["version"]+=1

        return model


    def best_model(self):

        if not self.models:
            return None

        return max(
            self.models,
            key=lambda x:self.models[x]["score"]
        )


evolution_core=AIEvolutionCore()
