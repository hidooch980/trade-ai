class AIDataLake:

    def __init__(self):
        self.datasets={}
        self.records=[]
        self.features={}


    def create_dataset(self,name,category):

        self.datasets[name]={
            "category":category,
            "status":"ACTIVE"
        }

        return self.datasets[name]


    def store_record(self,dataset,data):

        record={
            "dataset":dataset,
            "data":data
        }

        self.records.append(record)

        return record


    def create_feature(self,name,value):

        self.features[name]=value

        return {
            "feature":name,
            "status":"CREATED"
        }


    def status(self):

        return {
            "datasets":len(self.datasets),
            "records":len(self.records),
            "features":len(self.features),
            "lake":"ONLINE"
        }


data_lake=AIDataLake()
