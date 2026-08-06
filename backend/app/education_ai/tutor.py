class AITradingEducation:

    def __init__(self):
        self.users={}
        self.lessons={}
        self.reviews=[]


    def create_learning_profile(self,user,level):

        self.users[user]={
            "level":level,
            "progress":0
        }

        return self.users[user]


    def add_lesson(self,title,content):

        self.lessons[title]={
            "content":content,
            "status":"ACTIVE"
        }

        return self.lessons[title]


    def review_trade(self,user,trade):

        review={
            "user":user,
            "trade":trade,
            "analysis":"GENERATED"
        }

        self.reviews.append(review)

        return review


    def status(self):

        return {
            "students":len(self.users),
            "lessons":len(self.lessons),
            "reviews":len(self.reviews),
            "system":"ONLINE"
        }


education_ai=AITradingEducation()
