class AIUserPlatform:

    def __init__(self):
        self.users={}
        self.roles={}
        self.subscriptions={}
        self.referrals={}


    def create_user(self,user,role):

        self.users[user]={
            "role":role,
            "status":"ACTIVE"
        }

        return self.users[user]


    def assign_role(self,user,role):

        self.roles[user]=role

        return {
            "user":user,
            "role":role
        }


    def create_subscription(self,user,plan):

        self.subscriptions[user]={
            "plan":plan,
            "status":"ACTIVE"
        }

        return self.subscriptions[user]


    def add_referral(self,parent,child):

        self.referrals[child]=parent

        return {
            "child":child,
            "parent":parent
        }


    def status(self):

        return {
            "users":len(self.users),
            "subscriptions":len(self.subscriptions),
            "referrals":len(self.referrals),
            "platform":"ONLINE"
        }


user_platform=AIUserPlatform()
