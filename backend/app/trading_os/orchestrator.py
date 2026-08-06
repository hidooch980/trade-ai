class TradingOS:

    def __init__(self):
        self.mode="AUTONOMOUS"
        self.modules={}


    def register_module(self,name,status):

        self.modules[name]=status

        return {
            "module":name,
            "status":status
        }


    def health(self):

        return {
            "system":"AI_TRADING_OS",
            "mode":self.mode,
            "modules":self.modules
        }


    def decision(self,market,risk,strategy):

        if risk!="SAFE":
            return {
                "decision":"BLOCK",
                "reason":"RISK_CONTROL"
            }

        return {
            "decision":strategy,
            "market":market,
            "mode":self.mode
        }


trading_os=TradingOS()
