class AINeuralMarketMemory:

    def __init__(self):
        self.memories=[]
        self.patterns=[]
        self.matches=[]
        self.scores=[]


    def store_memory(self,data):

        item={
            "data":data,
            "status":"STORED"
        }

        self.memories.append(item)

        return item


    def detect_pattern(self,name,data):

        pattern={
            "name":name,
            "data":data
        }

        self.patterns.append(pattern)

        return pattern


    def find_match(self,current,history):

        match={
            "current":current,
            "history":history
        }

        self.matches.append(match)

        return match


    def score_pattern(self,pattern,score):

        item={
            "pattern":pattern,
            "score":score
        }

        self.scores.append(item)

        return item


    def status(self):

        return {
            "memories":len(self.memories),
            "patterns":len(self.patterns),
            "matches":len(self.matches),
            "scores":len(self.scores),
            "neural_memory":"ONLINE"
        }


neural_memory=AINeuralMarketMemory()
