class AIKnowledgeIntelligenceCenter:
    def __init__(self):
        self.documents=[]
        self.knowledge=[]
        self.searches=[]
        self.answers=[]

    def register_document(self,data):
        self.documents.append(data)

    def store_knowledge(self,data):
        self.knowledge.append(data)

    def search(self,data):
        self.searches.append(data)

    def generate_answer(self,data):
        self.answers.append(data)

    def status(self):
        return {
            "documents":len(self.documents),
            "knowledge_items":len(self.knowledge),
            "searches":len(self.searches),
            "answers":len(self.answers),
            "knowledge_engine":"ONLINE"
        }

knowledge_intelligence=AIKnowledgeIntelligenceCenter()
