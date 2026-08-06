class AIMarketPsychology:

    def __init__(self):
        self.sources=[]
        self.analysis=[]
        self.signals=[]


    def add_source(self,name):

        self.sources.append(name)

        return {
            "source":name,
            "status":"ACTIVE"
        }


    def analyze_sentiment(self,text,score):

        item={
            "text":text,
            "score":score
        }

        self.analysis.append(item)

        return item


    def create_signal(self,state):

        signal={
            "state":state,
            "status":"GENERATED"
        }

        self.signals.append(signal)

        return signal


    def status(self):

        return {
            "sources":len(self.sources),
            "analysis":len(self.analysis),
            "signals":len(self.signals),
            "psychology":"ONLINE"
        }


market_psychology=AIMarketPsychology()
