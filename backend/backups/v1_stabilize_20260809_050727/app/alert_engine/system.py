class AIAlertEngine:

    def __init__(self):
        self.alerts=[]
        self.channels={}
        self.preferences={}


    def register_channel(self,name,status):

        self.channels[name]={
            "status":status
        }

        return self.channels[name]


    def create_alert(self,event,priority):

        alert={
            "event":event,
            "priority":priority,
            "status":"CREATED"
        }

        self.alerts.append(alert)

        return alert


    def set_preference(self,user,level):

        self.preferences[user]={
            "level":level
        }

        return self.preferences[user]


    def status(self):

        return {
            "alerts":len(self.alerts),
            "channels":len(self.channels),
            "users":len(self.preferences),
            "engine":"ONLINE"
        }


alert_engine=AIAlertEngine()
