class AILiveRiskControl:

    def __init__(self):
        self.positions=[]
        self.limits=[]
        self.stops=[]
        self.alerts=[]

    def calculate_position(self,capital,risk):
        position={
            "capital":capital,
            "risk":risk
        }
        self.positions.append(position)
        return position

    def set_limit(self,item):
        self.limits.append(item)

    def set_stop(self,item):
        self.stops.append(item)

    def emergency_alert(self,item):
        self.alerts.append(item)

    def status(self):
        return {
            "positions":len(self.positions),
            "limits":len(self.limits),
            "stops":len(self.stops),
            "alerts":len(self.alerts),
            "risk_control":"ONLINE"
        }


live_risk_control = AILiveRiskControl()
