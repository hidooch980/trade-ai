class AIOptimizationEngine:

    def __init__(self):
        self.parameters=[]
        self.tests=[]
        self.optimizations=[]
        self.versions=[]


    def add_parameter(self,name,value):

        item={
            "name":name,
            "value":value
        }

        self.parameters.append(item)

        return item


    def run_test(self,model,result):

        item={
            "model":model,
            "result":result
        }

        self.tests.append(item)

        return item


    def optimize(self,target,result):

        item={
            "target":target,
            "result":result
        }

        self.optimizations.append(item)

        return item


    def save_version(self,name):

        version={
            "name":name,
            "status":"SAVED"
        }

        self.versions.append(version)

        return version


    def status(self):

        return {
            "parameters":len(self.parameters),
            "tests":len(self.tests),
            "optimizations":len(self.optimizations),
            "versions":len(self.versions),
            "optimization":"ONLINE"
        }


optimization_engine=AIOptimizationEngine()
