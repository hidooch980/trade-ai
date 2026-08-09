class AICloudInfrastructure:

    def __init__(self):
        self.services={}
        self.resources={}
        self.instances=[]


    def register_service(self,name):

        self.services[name]={
            "status":"RUNNING"
        }

        return self.services[name]


    def allocate_resource(self,service,resource):

        self.resources[service]=resource

        return {
            "service":service,
            "resource":resource,
            "status":"ALLOCATED"
        }


    def scale_instance(self,service,count):

        item={
            "service":service,
            "instances":count,
            "status":"SCALED"
        }

        self.instances.append(item)

        return item


    def status(self):

        return {
            "services":len(self.services),
            "resources":len(self.resources),
            "scales":len(self.instances),
            "cloud":"ONLINE"
        }


cloud_infrastructure=AICloudInfrastructure()
