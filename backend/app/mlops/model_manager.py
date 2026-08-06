class MLOpsManager:

    def __init__(self):
        self.models={}


    def register(self,name,version):

        self.models[name]={
            "version":version,
            "status":"REGISTERED",
            "performance":50
        }

        return self.models[name]


    def deploy(self,name):

        model=self.models.get(name)

        if not model:
            return None

        model["status"]="PRODUCTION"

        return model


    def monitor(self,name,score):

        model=self.models.get(name)

        if model:
            model["performance"]=score

            if score<40:
                model["status"]="REVIEW"

        return model


    def rollback(self,name):

        model=self.models.get(name)

        if model:
            model["status"]="ROLLBACK"

        return model


mlops=MLOpsManager()
