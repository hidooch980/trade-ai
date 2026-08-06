class AutonomousCorporation:

    def __init__(self):
        self.departments={}
        self.decisions=[]


    def create_department(self,name,agent):

        self.departments[name]={
            "agent":agent,
            "status":"ACTIVE"
        }

        return self.departments[name]


    def make_decision(self,topic,result):

        decision={
            "topic":topic,
            "result":result
        }

        self.decisions.append(decision)

        return decision


    def dashboard(self):

        return {
            "departments":len(self.departments),
            "decisions":len(self.decisions),
            "organization":"ACTIVE"
        }


autonomous_corporation=AutonomousCorporation()
