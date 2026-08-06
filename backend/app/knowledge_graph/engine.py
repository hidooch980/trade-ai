class AIKnowledgeGraph:

    def __init__(self):
        self.nodes={}
        self.relations=[]
        self.memory=[]


    def add_node(self,name,node_type,data):

        self.nodes[name]={
            "type":node_type,
            "data":data
        }

        return self.nodes[name]


    def add_relation(self,a,b,relation):

        item={
            "from":a,
            "to":b,
            "relation":relation
        }

        self.relations.append(item)

        return item


    def store_memory(self,event):

        self.memory.append(event)

        return {
            "status":"MEMORY_ADDED"
        }


    def status(self):

        return {
            "nodes":len(self.nodes),
            "relations":len(self.relations),
            "memory":len(self.memory),
            "graph":"ONLINE"
        }


knowledge_graph=AIKnowledgeGraph()
