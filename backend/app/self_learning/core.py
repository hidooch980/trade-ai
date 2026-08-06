class AISelfLearningEngine:

    def __init__(self):
        self.experiences=[]
        self.lessons=[]
        self.improvements=[]
        self.errors=[]


    def collect_experience(self,data):

        self.experiences.append(data)

        return {
            "status":"COLLECTED"
        }


    def analyze_lesson(self,lesson):

        self.lessons.append(lesson)

        return {
            "status":"ANALYZED"
        }


    def improve_model(self,change):

        self.improvements.append(change)

        return {
            "status":"IMPROVED"
        }


    def correct_error(self,error):

        self.errors.append(error)

        return {
            "status":"CORRECTED"
        }


    def status(self):

        return {
            "experiences":len(self.experiences),
            "lessons":len(self.lessons),
            "improvements":len(self.improvements),
            "errors":len(self.errors),
            "learning":"ONLINE"
        }


self_learning=AISelfLearningEngine()
