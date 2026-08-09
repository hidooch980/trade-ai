from app.ai.journal.trade_journal import trade_journal


class JournalConnector:

    def save_signal(self, result):

        decision = result["decision"]["decision"]

        return trade_journal.record(
            result["symbol"],
            decision,
            result["price"],
            result["risk"],
            result["smart_money"]
        )


journal_connector = JournalConnector()
