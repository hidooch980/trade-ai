class SocialTradingNetwork:

    def __init__(self):
        self.traders={}
        self.followers={}
        self.copy_accounts=[]


    def create_profile(self,name):

        self.traders[name]={
            "score":50,
            "followers":0
        }

        return self.traders[name]


    def follow(self,user,target):

        if target in self.traders:

            self.followers.setdefault(
                target,
                []
            ).append(user)

            self.traders[target]["followers"]+=1

            return {
                "status":"FOLLOWING"
            }

        return None


    def copy_trade(self,user,trader,capital):

        self.copy_accounts.append({
            "user":user,
            "trader":trader,
            "capital":capital
        })

        return {
            "status":"ACTIVE"
        }


    def ranking(self):

        return sorted(
            self.traders.items(),
            key=lambda x:x[1]["score"],
            reverse=True
        )


social_network=SocialTradingNetwork()
