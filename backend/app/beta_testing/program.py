class AIBetaTesting:

    def __init__(self):
        self.users=[]
        self.tests=[]
        self.feedback=[]


    def invite_user(self,user):

        self.users.append({
            "user":user,
            "status":"BETA"
        })

        return self.users[-1]


    def run_test(self,name,result):

        test={
            "name":name,
            "result":result
        }

        self.tests.append(test)

        return test


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
            "tests":len(self.tests),
            "feedback":len(self.feedback),
            "beta":"ACTIVE"
        }


beta_testing=AIBetaTesting()
