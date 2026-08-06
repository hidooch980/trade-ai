class AISystemCertification:

    def __init__(self):
        self.tests=[]
        self.results=[]
        self.certificates=[]
        self.issues=[]


    def run_test(self,name):

        test={
            "name":name,
            "status":"RUNNING"
        }

        self.tests.append(test)

        return test


    def add_result(self,test,result):

        item={
            "test":test,
            "result":result
        }

        self.results.append(item)

        return item


    def report_issue(self,issue):

        self.issues.append(issue)

        return {
            "status":"RECORDED"
        }


    def certify(self,version):

        certificate={
            "version":version,
            "status":"APPROVED"
        }

        self.certificates.append(certificate)

        return certificate


    def status(self):

        return {
            "tests":len(self.tests),
            "results":len(self.results),
            "issues":len(self.issues),
            "certificates":len(self.certificates),
            "certification":"ONLINE"
        }


system_certification=AISystemCertification()
