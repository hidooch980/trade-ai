import secrets


class APIGateway:

    def __init__(self):
        self.keys={}
        self.requests=[]


    def create_key(self,developer):

        key=secrets.token_hex(16)

        self.keys[developer]={
            "api_key":key,
            "status":"ACTIVE"
        }

        return self.keys[developer]


    def validate(self,developer,key):

        data=self.keys.get(developer)

        if not data:
            return False

        return data["api_key"]==key


    def request_log(self,endpoint):

        self.requests.append(endpoint)

        return {
            "endpoint":endpoint,
            "logged":True
        }


    def stats(self):

        return {
            "developers":len(self.keys),
            "requests":len(self.requests)
        }


api_gateway=APIGateway()
