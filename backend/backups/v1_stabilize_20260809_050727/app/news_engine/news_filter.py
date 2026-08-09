HIGH_IMPACT_EVENTS=["NFP","FOMC","CPI","INTEREST_RATE"]
def check_news(event=None):
    if event in HIGH_IMPACT_EVENTS:
        return {"trade_allowed":False,"reason":"HIGH_IMPACT_NEWS"}
    return {"trade_allowed":True,"reason":"CLEAR"}
