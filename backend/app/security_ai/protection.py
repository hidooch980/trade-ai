import time


class SecurityGuardian:

    def __init__(self):
        self.emergency_stop=False


    def check_trade(self,order):

        if self.emergency_stop:
            return {
                "approved":False,
                "reason":"EMERGENCY_STOP"
            }

        if not order.get("symbol"):
            return {
                "approved":False,
                "reason":"INVALID_SYMBOL"
            }

        return {
            "approved":True,
            "time":time.time()
        }


    def stop_all(self):
        self.emergency_stop=True
        return {
            "status":"LOCKED"
        }


    def resume(self):
        self.emergency_stop=False
        return {
            "status":"ACTIVE"
        }


security_guardian=SecurityGuardian()
