class CyberDefenseAI:

    def __init__(self):
        self.threats=[]


    def analyze_event(self,event):

        risk=0

        if event.get("failed_login",0)>5:
            risk+=50

        if event.get("unknown_device"):
            risk+=30

        status="SAFE"

        if risk>=50:
            status="THREAT"

            self.threats.append({
                "event":event,
                "risk":risk
            })


        return {
            "risk_score":risk,
            "status":status
        }


    def response(self,risk):

        if risk>=80:
            return {
                "action":"BLOCK"
            }

        if risk>=50:
            return {
                "action":"REVIEW"
            }

        return {
            "action":"ALLOW"
        }


    def report(self):

        return {
            "detected_threats":len(self.threats),
            "security":"ACTIVE"
        }


cyber_defense=CyberDefenseAI()
