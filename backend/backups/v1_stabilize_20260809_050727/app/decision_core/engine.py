class AIDecisionCore:

    def __init__(self):
        self.inputs=[]
        self.decisions=[]
        self.explanations=[]


    def add_input(self,source,data):

        item={
            "source":source,
            "data":data
        }

        self.inputs.append(item)

        return item


    def create_decision(self,data,confidence):

        decision={
            "data":data,
            "confidence":confidence,
            "status":"GENERATED"
        }

        self.decisions.append(decision)

        return decision


    def explain(self,decision,reason):

        item={
            "decision":decision,
            "reason":reason
        }

        self.explanations.append(item)

        return item


    def status(self):

        return {
            "inputs":len(self.inputs),
            "decisions":len(self.decisions),
            "explanations":len(self.explanations),
            "decision_core":"ONLINE"
        }


decision_core=AIDecisionCore()
