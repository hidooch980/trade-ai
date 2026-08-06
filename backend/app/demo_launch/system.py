class AIDemoLaunch:

    def __init__(self):
        self.users=[]
        self.sessions=[]
        self.results=[]


    def add_user(self,user):

        item={
            "user":user,
            "status":"DEMO_ACTIVE"
        }

        self.users.append(item)

        return item


    def create_session(self,user,broker):

        session={
            "user":user,
            "broker":broker,
            "status":"CONNECTED"
        }

        self.sessions.append(session)

        return session


    def record_result(self,test,result):

        item={
            "test":test,
            "result":result
        }

        self.results.append(item)

        return item


    def status(self):

        return {
            "users":len(self.users),
            "sessions":len(self.sessions),
            "results":len(self.results),
            "demo":"ONLINE"
        }


demo_launch=AIDemoLaunch()
