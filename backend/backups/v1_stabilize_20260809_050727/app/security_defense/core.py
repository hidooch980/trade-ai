class AISecurityDefense:

    def __init__(self):
        self.users=[]
        self.threats=[]
        self.incidents=[]


    def register_access(self,user,role):

        item={
            "user":user,
            "role":role,
            "status":"AUTHORIZED"
        }

        self.users.append(item)

        return item


    def detect_threat(self,data,level):

        threat={
            "data":data,
            "level":level,
            "status":"DETECTED"
        }

        self.threats.append(threat)

        return threat


    def create_incident(self,event):

        incident={
            "event":event,
            "status":"OPEN"
        }

        self.incidents.append(incident)

        return incident


    def status(self):

        return {
            "users":len(self.users),
            "threats":len(self.threats),
            "incidents":len(self.incidents),
            "security":"ONLINE"
        }


security_defense=AISecurityDefense()
