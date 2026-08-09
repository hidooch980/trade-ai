class TrailingStop:

    def update(self, position, distance=0.0005):
        current = position.get("current_price")
        entry = position.get("entry_price")

        if current is None or entry is None:
            return position

        if position.get("side") == "BUY":
            new_sl = current - distance

            if (
                position.get("stop_loss") is None
                or new_sl > position["stop_loss"]
            ):
                position["stop_loss"] = new_sl

        else:
            new_sl = current + distance

            if (
                position.get("stop_loss") is None
                or new_sl < position["stop_loss"]
            ):
                position["stop_loss"] = new_sl

        return position


trailing_stop = TrailingStop()
