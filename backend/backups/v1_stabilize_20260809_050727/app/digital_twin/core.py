class AIDigitalTwin:

    def __init__(self):
        self.markets=[]
        self.scenarios=[]
        self.simulations=[]
        self.results=[]


    def create_market_model(self,data):

        model={
            "data":data,
            "status":"CREATED"
        }

        self.markets.append(model)

        return model


    def generate_scenario(self,name,condition):

        scenario={
            "name":name,
            "condition":condition
        }

        self.scenarios.append(scenario)

        return scenario


    def simulate_strategy(self,strategy,scenario):

        simulation={
            "strategy":strategy,
            "scenario":scenario,
            "status":"RUNNING"
        }

        self.simulations.append(simulation)

        return simulation


    def save_result(self,result):

        self.results.append(result)

        return {
            "status":"STORED"
        }


    def status(self):

        return {
            "markets":len(self.markets),
            "scenarios":len(self.scenarios),
            "simulations":len(self.simulations),
            "results":len(self.results),
            "digital_twin":"ONLINE"
        }


digital_twin=AIDigitalTwin()
