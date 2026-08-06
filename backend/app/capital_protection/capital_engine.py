class CapitalProtection:

    def __init__(self):
        self.max_daily_loss=0.03
        self.max_weekly_loss=0.10
        self.max_monthly_loss=0.20

    def can_trade(self,current_loss):

        return current_loss < self.max_daily_loss

capital=CapitalProtection()
