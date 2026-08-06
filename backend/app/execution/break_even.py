class BreakEven:
    def update(self,position,trigger=10):
        if position["side"]=="BUY":
            if position["current_price"]-position["entry_price"]>=trigger and (position.get("stop_loss") is None or position["stop_loss"]<position["entry_price"]):
                position["stop_loss"]=position["entry_price"]
        else:
            if position["entry_price"]-position["current_price"]>=trigger and (position.get("stop_loss") is None or position["stop_loss"]>position["entry_price"]):
                position["stop_loss"]=position["entry_price"]
        return position

break_even=BreakEven()
