class AccessNetwork:

    def __init__(self):
        self.users={}
        self.subscriptions={}


    def register_user(self,user,owner=False):

        self.users[user]={
            "owner_member":owner,
            "status":"ACTIVE"
        }

        return self.users[user]


    def activate_subscription(self,user,plan):

        self.subscriptions[user]={
            "plan":plan,
            "status":"ACTIVE"
        }

        return self.subscriptions[user]


    def check_access(self,user):

        if user in self.users:
            if self.users[user]["owner_member"]:
                return {
                    "access":"FREE_NETWORK"
                }

        if user in self.subscriptions:
            return {
                "access":"PAID_SUBSCRIPTION"
            }

        return {
            "access":"PAYMENT_REQUIRED"
        }


    def status(self):

        return {
            "users":len(self.users),
            "subscriptions":len(self.subscriptions),
            "system":"ONLINE"
        }


access_network=AccessNetwork()
