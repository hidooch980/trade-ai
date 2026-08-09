class AITradingOS:

    def __init__(self):
        self.modules={}
        self.agents={}
        self.services={}


    def register_module(self,name,status):

        self.modules[name]={
            "status":status
        }

        return self.modules[name]


    def register_agent(self,name,role):

        self.agents[name]={
            "role":role,
            "status":"ONLINE"
        }

        return self.agents[name]


    def register_service(self,name):

        self.services[name]={
            "status":"RUNNING"
        }

        return self.services[name]


    def system_status(self):

        return {
            "modules":len(self.modules),
            "agents":len(self.agents),
            "services":len(self.services),
            "os":"ONLINE"
        }


trading_os=AITradingOS()
