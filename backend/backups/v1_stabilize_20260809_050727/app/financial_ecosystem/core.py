class FinancialEcosystem:

    def __init__(self):
        self.services={}
        self.users={}
        self.events=[]


    def register_service(self,name,service):

        self.services[name]={
            "service":service,
            "status":"ACTIVE"
        }

        return self.services[name]


    def create_profile(self,user,data):

        self.users[user]=data

        return self.users[user]


    def orchestrate(self,event):

        self.events.append(event)

        return {
            "event":event,
            "status":"COORDINATED"
        }


    def status(self):

        return {
            "services":len(self.services),
            "users":len(self.users),
            "ecosystem":"ONLINE"
        }


financial_ecosystem=FinancialEcosystem()
