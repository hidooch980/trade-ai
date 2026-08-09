class AIMobileIntelligence:

    def __init__(self):
        self.devices=[]
        self.notifications=[]
        self.sessions=[]


    def register_device(self,user,device):

        item={
            "user":user,
            "device":device,
            "status":"CONNECTED"
        }

        self.devices.append(item)

        return item


    def send_notification(self,user,message):

        notification={
            "user":user,
            "message":message,
            "status":"SENT"
        }

        self.notifications.append(notification)

        return notification


    def create_session(self,user):

        session={
            "user":user,
            "status":"ACTIVE"
        }

        self.sessions.append(session)

        return session


    def status(self):

        return {
            "devices":len(self.devices),
            "notifications":len(self.notifications),
            "sessions":len(self.sessions),
            "mobile":"ONLINE"
        }


mobile_intelligence=AIMobileIntelligence()
