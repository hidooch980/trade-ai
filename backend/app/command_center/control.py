class AICommandCenter:

    def __init__(self):
        self.modules={}
        self.alerts=[]


    def register_module(self,name,status):

        self.modules[name]={
            "status":status
        }

        return self.modules[name]


    def add_alert(self,message,level):

        alert={
            "message":message,
            "level":level
        }

        self.alerts.append(alert)

        return alert


    def system_status(self):

        return {
            "modules":len(self.modules),
            "alerts":len(self.alerts),
            "command_center":"ONLINE"
        }


command_center=AICommandCenter()
