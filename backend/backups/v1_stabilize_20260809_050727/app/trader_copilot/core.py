class AITraderCopilot:

    def __init__(self):
        self.users=[]
        self.messages=[]
        self.reports=[]


    def register_user(self,user):

        self.users.append(user)

        return {
            "user":user,
            "status":"REGISTERED"
        }


    def chat(self,user,message):

        item={
            "user":user,
            "message":message,
            "status":"PROCESSED"
        }

        self.messages.append(item)

        return item


    def create_report(self,user,data):

        report={
            "user":user,
            "data":data
        }

        self.reports.append(report)

        return report


    def status(self):

        return {
            "users":len(self.users),
            "messages":len(self.messages),
            "reports":len(self.reports),
            "copilot":"ONLINE"
        }


trader_copilot=AITraderCopilot()
