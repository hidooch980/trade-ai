class AIPublicLaunch:

    def __init__(self):
        self.users=[]
        self.plans={}
        self.feedback=[]


    def onboard_user(self,user):

        item={
            "user":user,
            "status":"ACTIVE"
        }

        self.users.append(item)

        return item


    def create_plan(self,name,features):

        self.plans[name]={
            "features":features,
            "status":"AVAILABLE"
        }

        return self.plans[name]


    def add_feedback(self,user,message):

        item={
            "user":user,
            "message":message
        }

        self.feedback.append(item)

        return item


    def status(self):

        return {
            "users":len(self.users),
            "plans":len(self.plans),
            "feedback":len(self.feedback),
            "launch":"ACTIVE"
        }


public_launch=AIPublicLaunch()
