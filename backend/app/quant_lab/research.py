class AIQuantLab:

    def __init__(self):
        self.models={}
        self.tests=[]
        self.results=[]


    def create_model(self,name,logic):

        self.models[name]={
            "logic":logic,
            "status":"CREATED"
        }

        return self.models[name]


    def backtest(self,model,data):

        result={
            "model":model,
            "data":data,
            "status":"TESTED"
        }

        self.tests.append(result)

        return result


    def evaluate(self,model,metrics):

        result={
            "model":model,
            "metrics":metrics
        }

        self.results.append(result)

        return result


    def status(self):

        return {
            "models":len(self.models),
            "tests":len(self.tests),
            "results":len(self.results),
            "lab":"ONLINE"
        }


quant_lab=AIQuantLab()
