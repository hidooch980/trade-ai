class AIMarketSentiment:

    def __init__(self):
        self.sources=[]
        self.sentiments=[]
        self.reports=[]


    def add_source(self,source):

        self.sources.append(source)

        return {
            "source":source,
            "status":"ACTIVE"
        }


    def analyze(self,text,score):

        item={
            "text":text,
            "score":score
        }

        self.sentiments.append(item)

        return item


    def generate_report(self,market,state):

        report={
            "market":market,
            "state":state
        }

        self.reports.append(report)

        return report


    def status(self):

        return {
            "sources":len(self.sources),
            "sentiments":len(self.sentiments),
            "reports":len(self.reports),
            "engine":"ONLINE"
        }


sentiment_engine=AIMarketSentiment()
