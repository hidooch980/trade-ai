class AICustomerIntelligenceCenter:
    def __init__(self):
        self.customers=[]
        self.behaviors=[]
        self.segments=[]
        self.insights=[]

    def register_customer(self,data):
        self.customers.append(data)

    def analyze_behavior(self,data):
        self.behaviors.append(data)

    def create_segment(self,data):
        self.segments.append(data)

    def generate_insight(self,data):
        self.insights.append(data)

    def status(self):
        return {
            "customers":len(self.customers),
            "behaviors":len(self.behaviors),
            "segments":len(self.segments),
            "insights":len(self.insights),
            "customer_engine":"ONLINE"
        }

customer_intelligence=AICustomerIntelligenceCenter()
