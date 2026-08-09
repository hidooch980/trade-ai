class AIOperationsCenter:
    def __init__(self):
        self.agents=[]
        self.workflows=[]
        self.tasks=[]
        self.incidents=[]

    def register_agent(self,data):
        self.agents.append(data)

    def create_workflow(self,data):
        self.workflows.append(data)

    def assign_task(self,data):
        self.tasks.append(data)

    def record_incident(self,data):
        self.incidents.append(data)

    def status(self):
        return {
            "agents":len(self.agents),
            "workflows":len(self.workflows),
            "tasks":len(self.tasks),
            "incidents":len(self.incidents),
            "operations_center":"ONLINE"
        }

ai_operations_center=AIOperationsCenter()
