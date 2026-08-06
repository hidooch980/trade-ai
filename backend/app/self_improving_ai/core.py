class SelfImprovingAI:

    def __init__(self):
        self.experiences=[]
        self.models={}
        self.changes=[]


    def add_experience(self,data):

        self.experiences.append(data)

        return {
            "status":"LEARNED"
        }


    def evaluate_model(self,name,score):

        self.models[name]={
            "score":score,
            "status":"EVALUATED"
        }

        return self.models[name]


    def improve_model(self,name,update):

        change={
            "model":name,
            "update":update,
            "status":"TESTING"
        }

        self.changes.append(change)

        return change


    def status(self):

        return {
            "experiences":len(self.experiences),
            "models":len(self.models),
            "changes":len(self.changes),
            "system":"ONLINE"
        }


self_improving_ai=SelfImprovingAI()
