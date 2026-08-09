class ProductionHardening:

    def __init__(self):
        self.checks=[]


    def add_check(self,name,status):

        self.checks.append({
            "name":name,
            "status":status
        })

        return self.checks[-1]


    def readiness(self):

        failed=[
            c for c in self.checks
            if c["status"]!="PASS"
        ]

        return {
            "checks":len(self.checks),
            "ready":len(failed)==0,
            "status":
            "PRODUCTION_READY"
            if not failed
            else "NEEDS_REVIEW"
        }


production_check=ProductionHardening()
