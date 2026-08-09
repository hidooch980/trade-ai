class EnterpriseUserManager:

    def __init__(self):
        self.users=[]
        self.roles=[]
        self.permissions=[]
        self.teams=[]

    def create_user(self,data):
        self.users.append(data)

    def assign_role(self,data):
        self.roles.append(data)

    def grant_permission(self,data):
        self.permissions.append(data)

    def create_team(self,data):
        self.teams.append(data)

    def status(self):
        return {
            "users":len(self.users),
            "roles":len(self.roles),
            "permissions":len(self.permissions),
            "teams":len(self.teams),
            "user_management":"ONLINE"
        }


enterprise_users=EnterpriseUserManager()
