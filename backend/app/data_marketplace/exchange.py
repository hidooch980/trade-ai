class DataMarketplace:

    def __init__(self):
        self.datasets={}
        self.purchases=[]


    def publish(self,name,owner,category):

        self.datasets[name]={
            "owner":owner,
            "category":category,
            "quality":50,
            "status":"AVAILABLE"
        }

        return self.datasets[name]


    def validate(self,name,score):

        dataset=self.datasets.get(name)

        if dataset:
            dataset["quality"]=score

        return dataset


    def purchase(self,user,dataset):

        if dataset in self.datasets:

            self.purchases.append({
                "user":user,
                "dataset":dataset
            })

            return {
                "status":"ACCESS_GRANTED"
            }

        return None


    def status(self):

        return {
            "datasets":len(self.datasets),
            "sales":len(self.purchases)
        }


data_marketplace=DataMarketplace()
