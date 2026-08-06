class AIVoiceTradingAssistant:

    def __init__(self):
        self.commands=[]
        self.languages=[]
        self.responses=[]


    def add_language(self,language):

        self.languages.append(language)

        return {
            "language":language,
            "status":"ACTIVE"
        }


    def process_command(self,user,voice_text):

        command={
            "user":user,
            "text":voice_text,
            "status":"PROCESSED"
        }

        self.commands.append(command)

        return command


    def create_response(self,text):

        response={
            "text":text,
            "status":"READY"
        }

        self.responses.append(response)

        return response


    def status(self):

        return {
            "commands":len(self.commands),
            "languages":len(self.languages),
            "responses":len(self.responses),
            "voice":"ONLINE"
        }


voice_assistant=AIVoiceTradingAssistant()
