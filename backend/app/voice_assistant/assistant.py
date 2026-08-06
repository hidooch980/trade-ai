class AIVoiceTradingAssistant:

    def __init__(self):
        self.users={}
        self.commands=[]
        self.responses=[]


    def register_user(self,user,voice_id):

        self.users[user]={
            "voice_id":voice_id,
            "status":"ACTIVE"
        }

        return self.users[user]


    def process_command(self,user,voice_text):

        command={
            "user":user,
            "text":voice_text,
            "status":"ANALYZED"
        }

        self.commands.append(command)

        return command


    def generate_response(self,message):

        response={
            "message":message,
            "status":"READY"
        }

        self.responses.append(response)

        return response


    def status(self):

        return {
            "users":len(self.users),
            "commands":len(self.commands),
            "assistant":"ONLINE"
        }


voice_assistant=AIVoiceTradingAssistant()
