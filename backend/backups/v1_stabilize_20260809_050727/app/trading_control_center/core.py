class AITradingControlCenter:

    def __init__(self):
        self.commands=[]
        self.monitors=[]
        self.operations=[]
        self.alerts=[]

    def execute_command(self,command):
        self.commands.append(command)
        return {
            "command":command,
            "status":"EXECUTED"
        }

    def monitor_system(self,data):
        self.monitors.append(data)

    def add_operation(self,item):
        self.operations.append(item)

    def alert(self,item):
        self.alerts.append(item)

    def status(self):
        return {
            "commands":len(self.commands),
            "monitors":len(self.monitors),
            "operations":len(self.operations),
            "alerts":len(self.alerts),
            "control_center":"ONLINE"
        }


trading_control_center=AITradingControlCenter()
