from app.ai.journal.trade_journal import trade_journal


class TradeResultUpdater:


    def update_result(
        self,
        index,
        exit_price,
        profit
    ):

        trades = trade_journal.history()


        if index >= len(trades):
            return None


        trades[index]["exit"] = exit_price
        trades[index]["profit"] = profit
        trades[index]["status"] = "CLOSED"


        trade_journal.file.write_text(
            __import__("json").dumps(
                trades,
                indent=4
            )
        )


        return trades[index]


trade_result_updater = TradeResultUpdater()
