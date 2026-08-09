class AIModelFactory:

    def __init__(self):
        self.models={}
        self.training_jobs=[]
        self.deployments=[]


    def create_training_job(self,name,data):

        job={
            "model":name,
            "data":data,
            "status":"TRAINING"
        }

        self.training_jobs.append(job)

        return job


    def register_model(self,name,version,score):

        self.models[name]={
            "version":version,
            "score":score,
            "status":"REGISTERED"
        }

        return self.models[name]


    def deploy_model(self,name):

        deployment={
            "model":name,
            "status":"DEPLOYED"
        }

        self.deployments.append(deployment)

        return deployment


    def status(self):

        return {
            "models":len(self.models),
            "training":len(self.training_jobs),
            "deployments":len(self.deployments),
            "factory":"ONLINE"
        }


model_factory=AIModelFactory()
