class AIRegulatoryIntelligence:

    def __init__(self):
        self.rules=[]
        self.checks=[]
        self.alerts=[]
        self.reports=[]


    def add_rule(self,name,details):

        rule={
            "name":name,
            "details":details
        }

        self.rules.append(rule)

        return rule


    def check_compliance(self,item,result):

        check={
            "item":item,
            "result":result
        }

        self.checks.append(check)

        return check


    def create_alert(self,message):

        self.alerts.append(message)

        return {
            "status":"ALERT_CREATED"
        }


    def generate_report(self,data):

        self.reports.append(data)

        return {
            "status":"REPORT_CREATED"
        }


    def status(self):

        return {
            "rules":len(self.rules),
            "checks":len(self.checks),
            "alerts":len(self.alerts),
            "reports":len(self.reports),
            "compliance":"ONLINE"
        }


regulatory_intelligence=AIRegulatoryIntelligence()
