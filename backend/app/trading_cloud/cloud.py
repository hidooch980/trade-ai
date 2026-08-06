class TradingCloud:

    def __init__(self):
        self.nodes={}
        self.services={}


    def add_node(self,name,region):

        self.nodes[name]={
            "region":region,
            "status":"ONLINE"
        }

        return self.nodes[name]


    def deploy_service(self,name):

        self.services[name]={
            "status":"RUNNING"
        }

        return self.services[name]


    def scale(self,load):

        if load>80:
            return {
                "action":"SCALE_UP"
            }

        return {
            "action":"NORMAL"
        }


    def status(self):

        return {
            "nodes":len(self.nodes),
            "services":len(self.services),
            "cloud":"ACTIVE"
        }


trading_cloud=TradingCloud()
