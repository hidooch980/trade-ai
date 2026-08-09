import time


class ObservabilityPlatform:

    def __init__(self):
        self.logs=[]
        self.services={}


    def register_service(self,name):

        self.services[name]={
            "status":"ONLINE",
            "last_check":time.time()
        }

        return self.services[name]


    def log(self,level,message):

        event={
            "level":level,
            "message":message,
            "time":time.time()
        }

        self.logs.append(event)

        return event


    def health(self):

        return {
            "services":len(self.services),
            "logs":len(self.logs),
            "status":"HEALTHY"
        }


    def alert(self,message):

        return {
            "alert":message,
            "sent":True
        }


observability=ObservabilityPlatform()
