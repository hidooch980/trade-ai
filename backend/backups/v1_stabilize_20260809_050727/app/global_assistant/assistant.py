class AIGlobalAssistant:

    def __init__(self):
        self.languages={}
        self.users={}
        self.messages=[]


    def add_language(self,language):

        self.languages[language]={
            "status":"SUPPORTED"
        }

        return self.languages[language]


    def create_context(self,user,data):

        self.users[user]=data

        return {
            "user":user,
            "status":"CONTEXT_CREATED"
        }


    def process_message(self,user,message):

        item={
            "user":user,
            "message":message,
            "status":"PROCESSED"
        }

        self.messages.append(item)

        return item


    def status(self):

        return {
            "languages":len(self.languages),
            "users":len(self.users),
            "messages":len(self.messages),
            "assistant":"ONLINE"
        }


global_assistant=AIGlobalAssistant()
