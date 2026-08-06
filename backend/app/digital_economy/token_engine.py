class DigitalEconomy:

    def __init__(self):
        self.accounts={}
        self.assets={}


    def create_account(self,user):

        self.accounts[user]={
            "points":0,
            "level":1
        }

        return self.accounts[user]


    def reward(self,user,points):

        account=self.accounts.get(user)

        if not account:
            return None

        account["points"]+=points

        if account["points"]>=1000:
            account["level"]+=1

        return account


    def register_asset(self,name,owner):

        self.assets[name]={
            "owner":owner,
            "status":"ACTIVE"
        }

        return self.assets[name]


    def stats(self):

        return {
            "accounts":len(self.accounts),
            "assets":len(self.assets)
        }


digital_economy=DigitalEconomy()
