class InstitutionalAI:

    def __init__(self):
        self.data=[]
        self.alerts=[]


    def analyze_flow(self,volume,buy,sell):

        pressure="NEUTRAL"

        if buy > sell:
            pressure="BUY_PRESSURE"

        if sell > buy:
            pressure="SELL_PRESSURE"

        result={
            "volume":volume,
            "pressure":pressure
        }

        self.data.append(result)

        return result


    def detect_smart_money(self,activity):

        if activity.get("large_order"):
            alert={
                "type":"SMART_MONEY_ACTIVITY",
                "status":"DETECTED"
            }

            self.alerts.append(alert)

            return alert

        return {
            "status":"NORMAL"
        }


    def status(self):

        return {
            "analyses":len(self.data),
            "alerts":len(self.alerts),
            "system":"ACTIVE"
        }


institutional_ai=InstitutionalAI()
