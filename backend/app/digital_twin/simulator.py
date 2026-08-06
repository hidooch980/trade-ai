class AIMarketDigitalTwin:

    def __init__(self):
        self.models=[]
        self.scenarios=[]
        self.simulations=[]


    def create_model(self,name,data):

        model={
            "name":name,
            "data":data,
            "status":"CREATED"
        }

        self.models.append(model)

        return model


    def add_scenario(self,name,condition):

        scenario={
            "name":name,
            "condition":condition
        }

        self.scenarios.append(scenario)

        return scenario


    def simulate(self,scenario,decision):

        result={
            "scenario":scenario,
            "decision":decision,
            "status":"SIMULATED"
        }

        self.simulations.append(result)

        return result


    def status(self):

        return {
            "models":len(self.models),
            "scenarios":len(self.scenarios),
            "simulations":len(self.simulations),
            "twin":"ONLINE"
        }


digital_twin=AIMarketDigitalTwin()
