class AIReleaseManager:

    def __init__(self):
        self.versions=[]
        self.deployments=[]
        self.tests=[]


    def create_version(self,version,notes):

        item={
            "version":version,
            "notes":notes,
            "status":"CREATED"
        }

        self.versions.append(item)

        return item


    def run_test(self,version,result):

        test={
            "version":version,
            "result":result
        }

        self.tests.append(test)

        return test


    def deploy(self,version):

        deployment={
            "version":version,
            "status":"DEPLOYED"
        }

        self.deployments.append(deployment)

        return deployment


    def status(self):

        return {
            "versions":len(self.versions),
            "tests":len(self.tests),
            "deployments":len(self.deployments),
            "release":"ONLINE"
        }


release_manager=AIReleaseManager()
