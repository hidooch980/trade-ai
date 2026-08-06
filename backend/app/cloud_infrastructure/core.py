class AICloudInfrastructure:

    def __init__(self):
        self.services=[]
        self.containers=[]
        self.resources=[]
        self.backups=[]


    def register_service(self,name):

        service={
            "name":name,
            "status":"RUNNING"
        }

        self.services.append(service)

        return service


    def create_container(self,name):

        container={
            "name":name,
            "status":"CREATED"
        }

        self.containers.append(container)

        return container


    def monitor_resource(self,data):

        self.resources.append(data)

        return {
            "status":"MONITORED"
        }


    def create_backup(self,name):

        self.backups.append(name)

        return {
            "backup":name,
            "status":"READY"
        }


    def status(self):

        return {
            "services":len(self.services),
            "containers":len(self.containers),
            "resources":len(self.resources),
            "backups":len(self.backups),
            "cloud":"ONLINE"
        }


cloud_infrastructure=AICloudInfrastructure()
