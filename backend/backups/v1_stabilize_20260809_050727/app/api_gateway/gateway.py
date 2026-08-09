class AIAPIGateway:

    def __init__(self):
        self.keys={}
        self.requests=[]


    def create_key(self,developer):

        key={
            "developer":developer,
            "status":"ACTIVE"
        }

        self.keys[developer]=key

        return key


    def request(self,developer,service):

        req={
            "developer":developer,
            "service":service,
            "status":"RECEIVED"
        }

        self.requests.append(req)

        return req


    def check_permission(self,developer):

        return {
            "developer":developer,
            "permission":"VERIFIED"
        }


    def status(self):

        return {
            "keys":len(self.keys),
            "requests":len(self.requests),
            "gateway":"ONLINE"
        }


api_gateway=AIAPIGateway()
