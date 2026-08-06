class EnterpriseDataGovernance:
    def __init__(self):
        self.datasets=[]
        self.rules=[]
        self.compliance=[]
        self.reports=[]

    def register_dataset(self,data):
        self.datasets.append(data)

    def add_rule(self,data):
        self.rules.append(data)

    def check_compliance(self,data):
        self.compliance.append(data)

    def create_report(self,data):
        self.reports.append(data)

    def status(self):
        return {
            "datasets":len(self.datasets),
            "rules":len(self.rules),
            "compliance_checks":len(self.compliance),
            "reports":len(self.reports),
            "governance":"ONLINE"
        }

data_governance=EnterpriseDataGovernance()
