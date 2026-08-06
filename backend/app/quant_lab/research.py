class QuantResearchLab:

    def __init__(self):
        self.models=[]


    def create_model(self,name,parameters):

        model={
            "name":name,
            "parameters":parameters,
            "score":50,
            "status":"TESTING"
        }

        self.models.append(model)
        return model


    def evaluate(self,name,metrics):

        for model in self.models:

            if model["name"]==name:

                score=(
                    metrics.get("win_rate",0)+
                    metrics.get("stability",0)
                )//2

                model["score"]=score
                model["status"]="READY" if score>=70 else "RESEARCH"

                return model

        return None


    def best_model(self):

        if not self.models:
            return None

        return max(
            self.models,
            key=lambda x:x["score"]
        )


quant_lab=QuantResearchLab()
