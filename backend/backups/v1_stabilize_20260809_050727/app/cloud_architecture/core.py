class AICloudArchitecture:

    def __init__(self):
        self.nodes=[]
        self.deployments=[]
        self.monitoring=[]
        self.loads=[]

    def register_node(self,name):
        self.nodes.append(name)

    def deploy(self,version):
        self.deployments.append(version)

    def monitor(self,data):
        self.monitoring.append(data)

    def balance(self,node):
        self.loads.append(node)

    def status(self):
        return {
            "nodes":len(self.nodes),
            "deployments":len(self.deployments),
            "monitoring":len(self.monitoring),
            "loads":len(self.loads),
            "cloud":"ONLINE"
        }

cloud_architecture = AICloudArchitecture()
