class VirtualTradingWorld:

    def __init__(self):
        self.users={}
        self.simulations=[]


    def create_user(self,name):

        self.users[name]={
            "avatar":"CREATED",
            "status":"ACTIVE"
        }

        return self.users[name]


    def start_simulation(self,scenario):

        simulation={
            "scenario":scenario,
            "status":"RUNNING"
        }

        self.simulations.append(simulation)

        return simulation


    def replay_market(self,event):

        return {
            "event":event,
            "mode":"REPLAY"
        }


    def status(self):

        return {
            "users":len(self.users),
            "simulations":len(self.simulations),
            "world":"ONLINE"
        }


virtual_market=VirtualTradingWorld()
