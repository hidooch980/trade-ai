class CyberDefenseAI:

    def __init__(self):
        self.events=[]
        self.alerts=[]


    def monitor(self,event):

        self.events.append(event)

        risk="LOW"

        if event.get("suspicious"):
            risk="HIGH"

            self.alerts.append({
                "event":event,
                "action":"REVIEW"
            })

        return {
            "risk":risk
        }


    def respond(self,alert):

        return {
            "alert":alert,
            "response":"PROCESSED"
        }


    def status(self):

        return {
            "events":len(self.events),
            "alerts":len(self.alerts),
            "security":"ACTIVE"
        }


cyber_defense=CyberDefenseAI()
