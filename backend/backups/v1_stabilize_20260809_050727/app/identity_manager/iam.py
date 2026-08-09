class IdentityManager:

    def __init__(self):
        self.users={}
        self.roles={}


    def create_user(self,user_id,role):

        self.users[user_id]={
            "role":role,
            "status":"ACTIVE",
            "permissions":[]
        }

        return self.users[user_id]


    def add_permission(self,user_id,permission):

        user=self.users.get(user_id)

        if not user:
            return None

        user["permissions"].append(permission)

        return user


    def authorize(self,user_id,permission):

        user=self.users.get(user_id)

        if not user:
            return False

        return permission in user["permissions"]


    def audit(self):

        return {
            "users":len(self.users),
            "security":"ACTIVE"
        }


iam=IdentityManager()
