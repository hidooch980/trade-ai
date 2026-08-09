class BreakEven:

    def update(self, position, trigger=0.0010):

        entry_price = position.get(
            "entry_price",
            position.get("entry")
        )

        if entry_price is None:
            return position

        current_price = position.get("current_price")

        if current_price is None:
            return position

        if position.get("side") == "BUY":

            if (
                current_price - entry_price >= trigger
                and (
                    position.get("stop_loss") is None
                    or position.get("stop_loss") < entry_price
                )
            ):
                position["stop_loss"] = entry_price

        else:

            if (
                entry_price - current_price >= trigger
                and (
                    position.get("stop_loss") is None
                    or position.get("stop_loss") > entry_price
                )
            ):
                position["stop_loss"] = entry_price

        return position


break_even = BreakEven()
