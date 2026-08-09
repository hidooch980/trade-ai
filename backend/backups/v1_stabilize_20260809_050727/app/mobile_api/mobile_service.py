class MobileTradingService:

    def __init__(self):
        self.devices={}


    def register_device(self,user,device):

        self.devices[user]={
            "device":device,
            "status":"ACTIVE"
        }

        return self.devices[user]


    def dashboard(self,user):

        return {
            "user":user,
            "balance":0,
            "profit":0,
            "risk":"LOW",
            "ai_status":"ONLINE"
        }


    def notify(self,user,message):

        return {
            "user":user,
            "message":message,
            "sent":True
        }


mobile_service=MobileTradingService()
