class AIKnowledgeFusion:

    def __init__(self):
        self.data_sources=[]
        self.knowledge=[]
        self.patterns=[]


    def add_source(self,name):

        self.data_sources.append(name)

        return {
            "source":name,
            "status":"CONNECTED"
        }


    def fuse_data(self,data):

        item={
            "data":data,
            "status":"FUSED"
        }

        self.knowledge.append(item)

        return item


    def detect_pattern(self,pattern):

        self.patterns.append(pattern)

        return {
            "pattern":pattern,
            "status":"FOUND"
        }


    def status(self):

        return {
            "sources":len(self.data_sources),
            "knowledge":len(self.knowledge),
            "patterns":len(self.patterns),
            "fusion":"ONLINE"
        }


knowledge_fusion=AIKnowledgeFusion()
