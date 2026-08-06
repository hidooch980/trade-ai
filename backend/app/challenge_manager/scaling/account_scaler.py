CHALLENGE_ACCOUNTS={2000:{"target":10,"daily_loss":5,"max_dd":10},5000:{"target":10,"daily_loss":5,"max_dd":10},10000:{"target":10,"daily_loss":5,"max_dd":10},25000:{"target":10,"daily_loss":5,"max_dd":10},50000:{"target":10,"daily_loss":5,"max_dd":10},100000:{"target":10,"daily_loss":5,"max_dd":10},200000:{"target":10,"daily_loss":5,"max_dd":10}}
def get_profile(balance):
    return CHALLENGE_ACCOUNTS.get(balance)
def risk_size(balance,risk_percent=1,stop_distance=10):
    risk=balance*(risk_percent/100)
    return round(max(risk/max(stop_distance,1),0.01),2)
