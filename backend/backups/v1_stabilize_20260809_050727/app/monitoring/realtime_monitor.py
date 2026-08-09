from datetime import datetime


class RealTimeMonitor:

    def __init__(self):

        self.events = []


    def record(
        self,
        event_type,
        data
    ):

        event = {

            "type": event_type,

            "data": data,

            "timestamp": datetime.now()

        }


        self.events.append(event)

        return event


    def status(self):

        return {

            "system": "ONLINE",

            "events": len(self.events),

            "last_event": (
                self.events[-1]
                if self.events
                else None
            )

        }
