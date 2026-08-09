import time


class DataStreamEngine:

    def __init__(self):
        self.events=[]
        self.subscribers=[]


    def publish(self,event):

        data={
            "event":event,
            "timestamp":time.time()
        }

        self.events.append(data)

        return data


    def subscribe(self,service):

        self.subscribers.append(service)

        return {
            "service":service,
            "subscribed":True
        }


    def process(self):

        return {
            "events":len(self.events),
            "subscribers":len(self.subscribers),
            "status":"RUNNING"
        }


stream_engine=DataStreamEngine()
