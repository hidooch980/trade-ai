class GlobalLaunchPlatform:

    def __init__(self):
        self.modules={}
        self.tests=[]


    def register_module(self,name):

        self.modules[name]={
            "status":"CONNECTED"
        }

        return self.modules[name]


    def run_test(self,name,result=True):

        test={
            "name":name,
            "result":"PASS" if result else "FAIL"
        }

        self.tests.append(test)

        return test


    def readiness(self):

        failed=[
            t for t in self.tests
            if t["result"]=="FAIL"
        ]

        return {
            "modules":len(self.modules),
            "tests":len(self.tests),
            "ready":len(failed)==0,
            "status":"READY" if not failed else "REVIEW"
        }


    def launch(self):

        return {
            "platform":"TRADE_AI",
            "launch":"ACTIVE"
        }


global_launch=GlobalLaunchPlatform()
