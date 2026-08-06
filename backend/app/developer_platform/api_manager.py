import secrets


class DeveloperPlatform:

    def __init__(self):
        self.keys={}
        self.apps={}


    def register_app(self,name):

        key=secrets.token_hex(16)

        self.apps[name]={
            "api_key":key,
            "status":"ACTIVE"
        }

        self.keys[key]=name

        return {
            "app":name,
            "api_key":key
        }


    def validate_key(self,key):

        return {
            "valid":key in self.keys
        }


    def usage(self,name):

        return {
            "app":name,
            "requests":"TRACKED"
        }


developer_platform=DeveloperPlatform()
