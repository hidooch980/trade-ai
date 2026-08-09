ACCOUNT_PROFILES={"MICRO_10":{"balance":10,"risk_percent":1,"max_daily_loss":2,"max_drawdown":5}}
def calculate_volume(balance,risk_percent,stop_distance):
    risk=balance*(risk_percent/100)
    return max(round(risk/max(stop_distance,1),2),0.01)
