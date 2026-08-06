class AIReleaseEngineering:

    def __init__(self):
        self.builds=[]
        self.packages=[]
        self.versions=[]
        self.deployments=[]


    def create_build(self,name):

        build={
            "name":name,
            "status":"BUILT"
        }

        self.builds.append(build)

        return build


    def create_package(self,components):

        package={
            "components":components,
            "status":"READY"
        }

        self.packages.append(package)

        return package


    def register_version(self,version):

        item={
            "version":version,
            "status":"REGISTERED"
        }

        self.versions.append(item)

        return item


    def deploy(self,target):

        deployment={
            "target":target,
            "status":"DEPLOYED"
        }

        self.deployments.append(deployment)

        return deployment


    def status(self):

        return {
            "builds":len(self.builds),
            "packages":len(self.packages),
            "versions":len(self.versions),
            "deployments":len(self.deployments),
            "release":"ONLINE"
        }


release_engineering=AIReleaseEngineering()
