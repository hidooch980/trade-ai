class AITradingCivilization:

    def __init__(self):
        self.entities={}
        self.knowledge=[]
        self.evolution=[]


    def register_entity(self,name,entity_type):

        self.entities[name]={
            "type":entity_type,
            "status":"ACTIVE"
        }

        return self.entities[name]


    def add_knowledge(self,data):

        self.knowledge.append(data)

        return {
            "status":"LEARNED"
        }


    def evolve(self,improvement):

        self.evolution.append(improvement)

        return {
            "status":"UPDATED"
        }


    def status(self):

        return {
            "entities":len(self.entities),
            "knowledge":len(self.knowledge),
            "civilization":"ACTIVE"
        }


ai_civilization=AITradingCivilization()
