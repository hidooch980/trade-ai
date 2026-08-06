class TrailingStop:
    def update(self, position, distance=5):
        if position["side"]=="BUY":
            new_sl=position["current_price"]-distance
            if position.get("stop_loss") is None or new_sl>position["stop_loss"]:
                position["stop_loss"]=new_sl
        else:
            new_sl=position["current_price"]+distance
            if position.get("stop_loss") is None or new_sl<position["stop_loss"]:
                position["stop_loss"]=new_sl
        return position

trailing_stop=TrailingStop()
