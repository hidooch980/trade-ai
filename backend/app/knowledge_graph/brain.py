class KnowledgeBrain:

    def __init__(self):
        self.nodes={}
        self.links=[]


    def add_knowledge(self,name,data):

        self.nodes[name]=data

        return self.nodes[name]


    def connect(self,source,target,relation):

        self.links.append({
            "source":source,
            "target":target,
            "relation":relation
        })

        return self.links[-1]


    def search(self,keyword):

        result=[]

        for key,value in self.nodes.items():

            if keyword.lower() in key.lower():
                result.append({
                    "name":key,
                    "data":value
                })

        return result


    def status(self):

        return {
            "nodes":len(self.nodes),
            "links":len(self.links),
            "brain":"ACTIVE"
        }


knowledge_brain=KnowledgeBrain()
