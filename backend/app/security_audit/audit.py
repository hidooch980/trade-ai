class AISecurityAudit:

    def __init__(self):
        self.tests=[]
        self.findings=[]
        self.reports=[]


    def run_test(self,name,result):

        test={
            "name":name,
            "result":result
        }

        self.tests.append(test)

        return test


    def add_finding(self,issue,level):

        finding={
            "issue":issue,
            "level":level
        }

        self.findings.append(finding)

        return finding


    def generate_report(self):

        report={
            "tests":len(self.tests),
            "findings":len(self.findings),
            "status":"GENERATED"
        }

        self.reports.append(report)

        return report


    def status(self):

        return {
            "tests":len(self.tests),
            "findings":len(self.findings),
            "reports":len(self.reports),
            "audit":"READY"
        }


security_audit=AISecurityAudit()
