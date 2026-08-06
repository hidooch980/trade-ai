class CloudInfrastructureManager:

    def __init__(self):
        self.nodes=[]
        self.services=[]
        self.resources=[]
        self.deployments=[]

    def register_node(self,data):
        self.nodes.append(data)

    def register_service(self,data):
        self.services.append(data)

    def allocate_resource(self,data):
        self.resources.append(data)

    def deploy(self,data):
        self.deployments.append(data)

    def status(self):
        return {
            "nodes":len(self.nodes),
            "services":len(self.services),
            "resources":len(self.resources),
            "deployments":len(self.deployments),
            "cloud_layer":"ONLINE"
        }


cloud_infrastructure=CloudInfrastructureManager()
