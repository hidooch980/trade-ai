class AIOperationsCenter:

    def __init__(self):
        self.services=[]
        self.alerts=[]
        self.events=[]

    def register_service(self,name,status):
        self.services.append({
            "service":name,
            "status":status
        })

    def create_alert(self,level,message):
        self.alerts.append({
            "level":level,
            "message":message
        })

    def log_event(self,event):
        self.events.append(event)

    def status(self):
        return {
            "services":len(self.services),
            "alerts":len(self.alerts),
            "events":len(self.events),
            "operations":"ONLINE"
        }


operations=AIOperationsCenter()
