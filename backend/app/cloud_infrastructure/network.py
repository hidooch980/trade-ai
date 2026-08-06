class AICloudInfrastructure:

    def __init__(self):
        self.nodes={}
        self.services={}


    def add_node(self,name,capacity):

        self.nodes[name]={
            "capacity":capacity,
            "status":"ONLINE"
        }

        return self.nodes[name]


    def register_service(self,name,node):

        self.services[name]={
            "node":node,
            "status":"RUNNING"
        }

        return self.services[name]


    def health_check(self):

        return {
            "nodes":len(self.nodes),
            "services":len(self.services),
            "status":"HEALTHY"
        }


    def status(self):

        return {
            "nodes":len(self.nodes),
            "services":len(self.services),
            "cloud":"ONLINE"
        }


cloud_infrastructure=AICloudInfrastructure()
