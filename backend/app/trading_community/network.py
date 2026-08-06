class TradingCommunity:

    def __init__(self):
        self.users={}
        self.posts=[]
        self.rankings={}


    def create_profile(self,user,data):

        self.users[user]={
            "data":data,
            "status":"ACTIVE"
        }

        return self.users[user]


    def publish(self,user,content):

        post={
            "user":user,
            "content":content,
            "status":"PUBLISHED"
        }

        self.posts.append(post)

        return post


    def rank_user(self,user,score):

        self.rankings[user]=score

        return {
            "user":user,
            "score":score
        }


    def status(self):

        return {
            "users":len(self.users),
            "posts":len(self.posts),
            "community":"ONLINE"
        }


trading_community=TradingCommunity()
