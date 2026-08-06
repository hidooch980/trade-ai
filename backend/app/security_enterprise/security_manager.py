import time
import hashlib

class EnterpriseSecurity:

    def __init__(self):
        self.events=[]


    def hash_secret(self,value):
        return hashlib.sha256(
            value.encode()
        ).hexdigest()


    def audit(self,event,user="SYSTEM"):

        record={
            "user":user,
            "event":event,
            "time":time.time()
        }

        self.events.append(record)
        return record


    def check_access(self,role,permission):

        allowed={
            "ADMIN":["ALL"],
            "MANAGER":["VIEW","TRADE","REPORT"],
            "TRADER":["VIEW","TRADE"]
        }

        return (
            permission in allowed.get(role,[])
            or "ALL" in allowed.get(role,[])
        )


security_manager=EnterpriseSecurity()
