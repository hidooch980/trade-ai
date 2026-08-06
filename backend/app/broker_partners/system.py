class BrokerPartnerSystem:

    def __init__(self):
        self.partners={}
        self.referrals=[]
        self.revenue=[]


    def add_partner(self,name,data):

        self.partners[name]={
            "data":data,
            "status":"ACTIVE"
        }

        return self.partners[name]


    def add_referral(self,user,broker):

        referral={
            "user":user,
            "broker":broker,
            "status":"TRACKED"
        }

        self.referrals.append(referral)

        return referral


    def record_revenue(self,broker,amount):

        item={
            "broker":broker,
            "amount":amount
        }

        self.revenue.append(item)

        return item


    def status(self):

        return {
            "partners":len(self.partners),
            "referrals":len(self.referrals),
            "revenue_records":len(self.revenue),
            "system":"ONLINE"
        }


broker_partner_system=BrokerPartnerSystem()
