class TradingAcademyAI:

    def __init__(self):
        self.students={}
        self.lessons={}
        self.progress={}


    def register_student(self,user,level):

        self.students[user]={
            "level":level,
            "status":"ACTIVE"
        }

        return self.students[user]


    def create_learning_path(self,user,path):

        self.progress[user]={
            "path":path,
            "completed":0
        }

        return self.progress[user]


    def update_progress(self,user,value):

        if user in self.progress:
            self.progress[user]["completed"]=value

        return self.progress.get(user)


    def evaluate(self,user):

        return {
            "user":user,
            "skill":"ANALYZED"
        }


    def status(self):

        return {
            "students":len(self.students),
            "paths":len(self.progress),
            "academy":"ONLINE"
        }


trading_academy=TradingAcademyAI()
