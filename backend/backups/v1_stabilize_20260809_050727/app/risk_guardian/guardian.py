class AIRiskGuardian:

    def __init__(self):
        self.risks=[]
        self.alerts=[]
        self.rules={}


    def analyze_risk(self,data):

        result={
            "data":data,
            "risk":"ANALYZED"
        }

        self.risks.append(result)

        return result


    def create_alert(self,message,level):

        alert={
            "message":message,
            "level":level
        }

        self.alerts.append(alert)

        return alert


    def add_rule(self,name,rule):

        self.rules[name]=rule

        return {
            "rule":name,
            "status":"ACTIVE"
        }


    def status(self):

        return {
            "risks":len(self.risks),
            "alerts":len(self.alerts),
            "rules":len(self.rules),
            "guardian":"ONLINE"
        }


risk_guardian=AIRiskGuardian()
