class AIMonitoringCenter:

    def __init__(self):
        self.services=[]
        self.alerts=[]
        self.logs=[]


    def register_service(self,name,status):

        item={
            "service":name,
            "status":status
        }

        self.services.append(item)

        return item


    def create_alert(self,level,message):

        alert={
            "level":level,
            "message":message,
            "status":"ACTIVE"
        }

        self.alerts.append(alert)

        return alert


    def add_log(self,data):

        self.logs.append(data)

        return {
            "status":"LOGGED"
        }


    def status(self):

        return {
            "services":len(self.services),
            "alerts":len(self.alerts),
            "logs":len(self.logs),
            "monitor":"ONLINE"
        }


monitoring_center=AIMonitoringCenter()
