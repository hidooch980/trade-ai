class CopyTradingNetwork:

    def __init__(self):
        self.masters={}
        self.followers={}


    def register_master(self,name,performance):

        self.masters[name]={
            "performance":performance,
            "status":"ACTIVE"
        }

        return self.masters[name]


    def rank_masters(self):

        return sorted(
            self.masters.items(),
            key=lambda x:x[1]["performance"],
            reverse=True
        )


    def follow(self,follower,master,capital):

        self.followers[follower]={
            "master":master,
            "capital":capital,
            "status":"COPYING"
        }

        return self.followers[follower]


    def status(self):

        return {
            "masters":len(self.masters),
            "followers":len(self.followers)
        }


copy_network=CopyTradingNetwork()
