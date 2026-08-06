class TradingDataMarketplace:

    def __init__(self):
        self.datasets={}
        self.providers={}


    def register_provider(self,name):

        self.providers[name]={
            "status":"ACTIVE"
        }

        return self.providers[name]


    def add_dataset(self,name,data_type,owner):

        self.datasets[name]={
            "type":data_type,
            "owner":owner,
            "status":"AVAILABLE"
        }

        return self.datasets[name]


    def evaluate_data(self,name):

        if name in self.datasets:
            self.datasets[name]["quality"]="ANALYZED"

        return self.datasets.get(name)


    def status(self):

        return {
            "datasets":len(self.datasets),
            "providers":len(self.providers),
            "marketplace":"ONLINE"
        }


data_marketplace=TradingDataMarketplace()
