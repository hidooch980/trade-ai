class AIUnifiedExperience:

    def __init__(self):
        self.users={}
        self.sessions=[]
        self.actions=[]


    def create_session(self,user):

        session={
            "user":user,
            "status":"ACTIVE"
        }

        self.sessions.append(session)

        return session


    def sync_context(self,user,data):

        self.users[user]=data

        return {
            "user":user,
            "status":"SYNCED"
        }


    def record_action(self,user,action):

        item={
            "user":user,
            "action":action
        }

        self.actions.append(item)

        return item


    def status(self):

        return {
            "users":len(self.users),
            "sessions":len(self.sessions),
            "actions":len(self.actions),
            "experience":"ONLINE"
        }


unified_experience=AIUnifiedExperience()
