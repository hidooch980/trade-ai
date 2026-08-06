class AISecurityGuardian:

    def __init__(self):
        self.events=[]
        self.threats=[]


    def monitor_event(self,event):

        self.events.append(event)

        return {
            "event":event,
            "status":"MONITORED"
        }


    def detect_threat(self,data):

        threat={
            "data":data,
            "level":"ANALYZED"
        }

        self.threats.append(threat)

        return threat


    def verify_access(self,user,permission):

        return {
            "user":user,
            "permission":permission,
            "status":"CHECKED"
        }


    def status(self):

        return {
            "events":len(self.events),
            "threats":len(self.threats),
            "security":"ACTIVE"
        }


security_guardian=AISecurityGuardian()
