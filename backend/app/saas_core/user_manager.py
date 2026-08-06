class UserManager:

    def __init__(self):
        self.users={}


    def create(self,user_id,role="CUSTOMER"):

        self.users[user_id]={
            "role":role,
            "active":True,
            "plan":"BASIC"
        }

        return self.users[user_id]


    def upgrade(self,user_id,plan):

        if user_id in self.users:
            self.users[user_id]["plan"]=plan

        return self.users.get(user_id)


    def check_access(self,user_id):

        user=self.users.get(user_id)

        if not user:
            return False

        return user["active"]


user_manager=UserManager()
