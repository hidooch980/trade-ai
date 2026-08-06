class MLTrainingPlatform:

    def __init__(self):
        self.datasets={}
        self.models={}


    def add_dataset(self,name,size):

        self.datasets[name]={
            "size":size,
            "status":"READY"
        }

        return self.datasets[name]


    def train(self,name,dataset):

        model={
            "model":name,
            "dataset":dataset,
            "accuracy":50,
            "status":"TRAINED"
        }

        self.models[name]=model

        return model


    def evaluate(self,name,score):

        model=self.models.get(name)

        if not model:
            return None

        model["accuracy"]=score

        return model


    def registry(self):

        return {
            "datasets":len(self.datasets),
            "models":len(self.models)
        }


ml_training=MLTrainingPlatform()
