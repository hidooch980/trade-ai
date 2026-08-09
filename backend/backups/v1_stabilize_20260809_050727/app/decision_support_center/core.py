class AIDecisionSupportCenter:
    def __init__(self):
        self.decisions=[]
        self.recommendations=[]
        self.rules=[]
        self.evaluations=[]

    def create_decision(self,data):
        self.decisions.append(data)

    def generate_recommendation(self,data):
        self.recommendations.append(data)

    def add_rule(self,data):
        self.rules.append(data)

    def evaluate(self,data):
        self.evaluations.append(data)

    def status(self):
        return {
            "decisions":len(self.decisions),
            "recommendations":len(self.recommendations),
            "rules":len(self.rules),
            "evaluations":len(self.evaluations),
            "decision_center":"ONLINE"
        }

ai_decision_support=AIDecisionSupportCenter()
