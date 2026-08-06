class TradingCommunity:

    def __init__(self):
        self.users={}
        self.posts=[]


    def create_profile(self,user):

        self.users[user]={
            "followers":0,
            "reputation":50,
            "level":"TRADER"
        }

        return self.users[user]


    def publish(self,user,content):

        post={
            "user":user,
            "content":content,
            "likes":0
        }

        self.posts.append(post)

        return post


    def like(self,index):

        if index < len(self.posts):
            self.posts[index]["likes"]+=1

        return self.posts[index]


    def ranking(self):

        return sorted(
            self.users.items(),
            key=lambda x:x[1]["reputation"],
            reverse=True
        )


community=TradingCommunity()
