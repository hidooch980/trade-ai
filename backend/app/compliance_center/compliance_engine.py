class ComplianceEngine:

    def __init__(self):
        self.rules={}


    def add_rule(self,name,value):

        self.rules[name]=value

        return {
            "rule":name,
            "status":"ACTIVE"
        }


    def check(self,user,action):

        violations=[]

        if action.get("volume",0)>action.get("max_volume",999999):
            violations.append("VOLUME_LIMIT")

        return {
            "user":user,
            "approved":len(violations)==0,
            "violations":violations
        }


    def report(self):

        return {
            "rules":len(self.rules),
            "system":"COMPLIANCE_ACTIVE"
        }


compliance_engine=ComplianceEngine()
