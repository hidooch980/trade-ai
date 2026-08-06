class FraudDetectionAI:

    def analyze(self,account,trades):

        risk_score=0
        alerts=[]

        if len(trades)>100:
            risk_score+=30
            alerts.append("OVER_TRADING")

        for trade in trades:
            if trade.get("volume",0)>account.get("max_volume",100):
                risk_score+=40
                alerts.append("HIGH_VOLUME")

        status="SAFE"

        if risk_score>=50:
            status="WARNING"

        if risk_score>=80:
            status="BLOCKED"

        return {
            "account":account.get("id"),
            "risk_score":risk_score,
            "status":status,
            "alerts":alerts
        }


fraud_ai=FraudDetectionAI()
