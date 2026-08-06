class AICommandCenter:

    def __init__(self):
        self.commands=[]
        self.agents=[]
        self.brokers=[]
        self.audit=[]


    def register_agent(self,name):

        agent={
            "name":name,
            "status":"MANAGED"
        }

        self.agents.append(agent)

        return agent


    def register_broker(self,name):

        broker={
            "name":name,
            "status":"CONNECTED"
        }

        self.brokers.append(broker)

        return broker


    def execute_command(self,command):

        item={
            "command":command,
            "status":"EXECUTED"
        }

        self.commands.append(item)

        return item


    def audit_action(self,action):

        self.audit.append(action)

        return {
            "status":"LOGGED"
        }


    def status(self):

        return {
            "commands":len(self.commands),
            "agents":len(self.agents),
            "brokers":len(self.brokers),
            "audit":len(self.audit),
            "command_center":"ONLINE"
        }


command_center=AICommandCenter()
