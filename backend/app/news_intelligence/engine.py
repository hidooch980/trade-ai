class AINewsIntelligence:

    def __init__(self):
        self.sources=[]
        self.news=[]
        self.events=[]
        self.analysis=[]


    def add_source(self,name):

        self.sources.append(name)

        return {
            "source":name,
            "status":"ACTIVE"
        }


    def collect_news(self,title,data):

        item={
            "title":title,
            "data":data
        }

        self.news.append(item)

        return item


    def analyze_impact(self,news,impact):

        item={
            "news":news,
            "impact":impact
        }

        self.analysis.append(item)

        return item


    def add_event(self,event):

        self.events.append(event)

        return {
            "event":event,
            "status":"TRACKING"
        }


    def status(self):

        return {
            "sources":len(self.sources),
            "news":len(self.news),
            "events":len(self.events),
            "analysis":len(self.analysis),
            "engine":"ONLINE"
        }


news_engine=AINewsIntelligence()
