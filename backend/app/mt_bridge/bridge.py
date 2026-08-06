class AIMetaTraderBridge:

    def __init__(self):
        self.terminals={}
        self.signals=[]
        self.executions=[]


    def register_terminal(self,user,platform):

        self.terminals[user]={
            "platform":platform,
            "status":"CONNECTED"
        }

        return self.terminals[user]


    def send_signal(self,user,signal):

        item={
            "user":user,
            "signal":signal,
            "status":"READY"
        }

        self.signals.append(item)

        return item


    def execute(self,user,order):

        execution={
            "user":user,
            "order":order,
            "status":"REQUESTED"
        }

        self.executions.append(execution)

        return execution


    def status(self):

        return {
            "terminals":len(self.terminals),
            "signals":len(self.signals),
            "executions":len(self.executions),
            "bridge":"ONLINE"
        }


mt_bridge=AIMetaTraderBridge()
