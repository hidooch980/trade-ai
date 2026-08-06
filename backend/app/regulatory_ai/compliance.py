class RegulatoryAI:

    def __init__(self):
        self.rules={}
        self.violations=[]


    def add_rule(self,country,rule):

        self.rules[country]=rule

        return {
            "country":country,
            "status":"ACTIVE"
        }


    def check(self,user,activity):

        violations=[]

        limit=self.rules.get(
            activity.get("country"),
            {}
        ).get("max_volume",None)


        if limit and activity.get("volume",0)>limit:
            violations.append(
                "VOLUME_LIMIT"
            )


        result={
            "user":user,
            "approved":len(violations)==0,
            "violations":violations
        }

        if violations:
            self.violations.append(result)

        return result


    def report(self):

        return {
            "rules":len(self.rules),
            "violations":len(self.violations),
            "system":"ACTIVE"
        }


regulatory_ai=RegulatoryAI()
