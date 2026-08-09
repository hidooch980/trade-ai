class EnterpriseSecurityManager:
    def __init__(self):
        self.identities=[]
        self.tokens=[]
        self.policies=[]
        self.audit=[]

    def register_identity(self,data):
        self.identities.append(data)

    def create_token(self,data):
        self.tokens.append(data)

    def add_policy(self,data):
        self.policies.append(data)

    def audit_event(self,data):
        self.audit.append(data)

    def status(self):
        return {
            "identities":len(self.identities),
            "tokens":len(self.tokens),
            "policies":len(self.policies),
            "audit_events":len(self.audit),
            "security":"ONLINE"
        }

enterprise_security=EnterpriseSecurityManager()
