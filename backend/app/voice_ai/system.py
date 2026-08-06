class AIVoiceSystem:

    def __init__(self):
        self.users={}
        self.commands=[]
        self.responses=[]


    def register_user(self,user,voice_profile):

        self.users[user]={
            "profile":voice_profile,
            "status":"ACTIVE"
        }

        return self.users[user]


    def process_command(self,user,command):

        item={
            "user":user,
            "command":command,
            "status":"PROCESSED"
        }

        self.commands.append(item)

        return item


    def generate_response(self,user,response):

        item={
            "user":user,
            "response":response,
            "status":"READY"
        }

        self.responses.append(item)

        return item


    def status(self):

        return {
            "users":len(self.users),
            "commands":len(self.commands),
            "responses":len(self.responses),
            "voice":"ONLINE"
        }


voice_ai=AIVoiceSystem()
