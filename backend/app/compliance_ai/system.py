class AIComplianceSystem:

    def __init__(self):
        self.rules={}
        self.logs=[]
        self.alerts=[]


    def add_rule(self,name,rule):

        self.rules[name]={
            "rule":rule,
            "status":"ACTIVE"
        }

        return self.rules[name]


    def audit(self,action,data):

        log={
            "action":action,
            "data":data
        }

        self.logs.append(log)

        return log


    def create_alert(self,message):

        alert={
            "message":message,
            "status":"OPEN"
        }

        self.alerts.append(alert)

        return alert


    def status(self):

        return {
            "rules":len(self.rules),
            "logs":len(self.logs),
            "alerts":len(self.alerts),
            "system":"ONLINE"
        }


compliance_ai=AIComplianceSystem()
