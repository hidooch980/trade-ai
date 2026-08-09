class GlobalDataFusion:

    def __init__(self):
        self.sources={}


    def add_source(self,name,value):

        self.sources[name]=value

        return {
            "source":name,
            "status":"ACTIVE"
        }


    def analyze(self):

        if not self.sources:
            return {
                "score":50,
                "decision":"WAIT"
            }

        score=sum(self.sources.values())//len(self.sources)

        decision="BUY" if score>=70 else (
            "SELL" if score<=30 else "WAIT"
        )

        return {
            "score":score,
            "decision":decision,
            "sources":self.sources
        }


global_intelligence=GlobalDataFusion()
