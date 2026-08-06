class AISimulationLab:

    def __init__(self):
        self.scenarios={}
        self.tests=[]
        self.results=[]


    def create_scenario(self,name,data):

        self.scenarios[name]={
            "data":data,
            "status":"READY"
        }

        return self.scenarios[name]


    def run_test(self,strategy,scenario):

        result={
            "strategy":strategy,
            "scenario":scenario,
            "status":"COMPLETED"
        }

        self.tests.append(result)

        return result


    def compare(self,results):

        item={
            "comparison":results,
            "status":"GENERATED"
        }

        self.results.append(item)

        return item


    def status(self):

        return {
            "scenarios":len(self.scenarios),
            "tests":len(self.tests),
            "reports":len(self.results),
            "lab":"ONLINE"
        }


simulation_lab=AISimulationLab()
