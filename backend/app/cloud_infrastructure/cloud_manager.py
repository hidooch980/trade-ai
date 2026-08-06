class CloudInfrastructure:

    def __init__(self):
        self.services={}


    def register_service(self,name,status="ONLINE"):

        self.services[name]={
            "status":status,
            "health":"GOOD"
        }

        return self.services[name]


    def health_check(self):

        online=0

        for service in self.services.values():
            if service["status"]=="ONLINE":
                online+=1

        return {
            "services":len(self.services),
            "online":online,
            "system":"HEALTHY"
        }


    def recover(self,name):

        if name in self.services:
            self.services[name]["status"]="ONLINE"
            self.services[name]["health"]="RECOVERED"

        return self.services.get(name)


cloud_manager=CloudInfrastructure()
