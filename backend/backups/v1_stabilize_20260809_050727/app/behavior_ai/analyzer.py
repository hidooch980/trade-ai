class AIBehaviorAnalyzer:

    def __init__(self):
        self.users={}
        self.patterns=[]
        self.feedback=[]


    def create_profile(self,user):

        self.users[user]={
            "style":"UNKNOWN",
            "status":"LEARNING"
        }

        return self.users[user]


    def analyze_action(self,user,action):

        pattern={
            "user":user,
            "action":action,
            "status":"ANALYZED"
        }

        self.patterns.append(pattern)

        return pattern


    def give_feedback(self,user,message):

        item={
            "user":user,
            "message":message
        }

        self.feedback.append(item)

        return item


    def status(self):

        return {
            "users":len(self.users),
            "patterns":len(self.patterns),
            "feedback":len(self.feedback),
            "system":"ONLINE"
        }


behavior_ai=AIBehaviorAnalyzer()
