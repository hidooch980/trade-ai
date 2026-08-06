class AIControlCenter:

    def __init__(self):
        self.widgets={}
        self.alerts=[]
        self.commands=[]


    def add_widget(self,name,data):

        self.widgets[name]=data

        return {
            "widget":name,
            "status":"ACTIVE"
        }


    def create_alert(self,message,level):

        alert={
            "message":message,
            "level":level
        }

        self.alerts.append(alert)

        return alert


    def execute_command(self,command):

        item={
            "command":command,
            "status":"QUEUED"
        }

        self.commands.append(item)

        return item


    def status(self):

        return {
            "widgets":len(self.widgets),
            "alerts":len(self.alerts),
            "commands":len(self.commands),
            "center":"ONLINE"
        }


control_center=AIControlCenter()
