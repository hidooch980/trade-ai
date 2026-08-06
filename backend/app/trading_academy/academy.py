class TradingAcademy:

    def __init__(self):
        self.students={}
        self.courses=[]


    def add_course(self,title,level):

        course={
            "title":title,
            "level":level,
            "status":"ACTIVE"
        }

        self.courses.append(course)

        return course


    def register_student(self,user):

        self.students[user]={
            "level":1,
            "score":0,
            "courses":[]
        }

        return self.students[user]


    def evaluate(self,user,score):

        student=self.students.get(user)

        if not student:
            return None

        student["score"]+=score

        if student["score"]>=100:
            student["level"]+=1

        return student


    def mentor(self,user):

        return {
            "user":user,
            "advice":"CONTINUE_LEARNING",
            "ai":"ACTIVE"
        }


academy=TradingAcademy()
