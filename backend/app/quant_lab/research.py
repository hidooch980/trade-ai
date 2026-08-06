class QuantResearchLab:

    def __init__(self):
        self.models={}


    def create_model(self,name,parameters):

        self.models[name]={
            "parameters":parameters,
            "score":50,
            "status":"RESEARCH"
        }

        return self.models[name]


    def evaluate(self,name,performance):

        model=self.models.get(name)

        if not model:
            return None

        if performance>0:
            model["score"]=min(
                model["score"]+10,
                100
            )
        else:
            model["score"]=max(
                model["score"]-10,
                0
            )

        model["status"]="TESTED"

        return model


    def best_model(self):

        if not self.models:
            return None

        return max(
            self.models,
            key=lambda x:self.models[x]["score"]
        )


quant_lab=QuantResearchLab()
