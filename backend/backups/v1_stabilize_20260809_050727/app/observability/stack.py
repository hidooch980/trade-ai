class AIObservabilityStack:

    def __init__(self):
        self.metrics={}
        self.logs=[]
        self.traces=[]


    def record_metric(self,name,value):

        self.metrics[name]=value


    def add_log(self,level,message):

        self.logs.append({
            "level":level,
            "message":message
        })


    def add_trace(self,event):

        self.traces.append(event)


    def report(self):

        return {
            "metrics":len(self.metrics),
            "logs":len(self.logs),
            "traces":len(self.traces),
            "observability":"ONLINE"
        }


observability=AIObservabilityStack()
