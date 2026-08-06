class AIIntelligenceNetwork:

    def __init__(self):
        self.nodes={}
        self.messages=[]
        self.memory=[]


    def register_node(self,name,node_type):

        self.nodes[name]={
            "type":node_type,
            "status":"CONNECTED"
        }

        return self.nodes[name]


    def send_message(self,source,target,message):

        item={
            "source":source,
            "target":target,
            "message":message
        }

        self.messages.append(item)

        return item


    def store_memory(self,data):

        self.memory.append(data)

        return {
            "status":"STORED"
        }


    def status(self):

        return {
            "nodes":len(self.nodes),
            "messages":len(self.messages),
            "memory":len(self.memory),
            "network":"ONLINE"
        }


intelligence_network=AIIntelligenceNetwork()
