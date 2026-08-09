class FraudDetector:

    def __init__(self):
        self.events=[]


    def analyze(self,user,activity):

        risk=0
        reasons=[]

        if activity.get("volume",0)>100:
            risk+=40
            reasons.append("HIGH_VOLUME")

        if activity.get("login_country_change"):
            risk+=30
            reasons.append("LOCATION_CHANGE")

        status="SAFE"

        if risk>=50:
            status="SUSPICIOUS"

        event={
            "user":user,
            "risk_score":risk,
            "status":status,
            "reasons":reasons
        }

        self.events.append(event)

        return event


    def report(self):

        return {
            "events":len(self.events),
            "security":"ACTIVE"
        }


fraud_detector=FraudDetector()
