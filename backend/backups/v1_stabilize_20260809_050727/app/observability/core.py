class AIObservabilityPlatform:

    def __init__(self):
        self.metrics=[]
        self.logs=[]
        self.alerts=[]
        self.incidents=[]


    def record_metric(self,name,value):

        item={
            "name":name,
            "value":value
        }

        self.metrics.append(item)

        return item


    def add_log(self,level,message):

        item={
            "level":level,
            "message":message
        }

        self.logs.append(item)

        return item


    def create_alert(self,message):

        alert={
            "message":message,
            "status":"ACTIVE"
        }

        self.alerts.append(alert)

        return alert


    def register_incident(self,incident):

        self.incidents.append(incident)

        return {
            "status":"TRACKED"
        }


    def status(self):

        return {
            "metrics":len(self.metrics),
            "logs":len(self.logs),
            "alerts":len(self.alerts),
            "incidents":len(self.incidents),
            "observability":"ONLINE"
        }


observability=AIObservabilityPlatform()
