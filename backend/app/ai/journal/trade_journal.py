import json
from pathlib import Path
from datetime import datetime


class TradeJournal:

    def __init__(self):
        self.file = Path(
            "data/trade_journal.json"
        )

        self.file.parent.mkdir(
            exist_ok=True
        )

        if not self.file.exists():
            self.file.write_text("[]")


    def record(
        self,
        symbol,
        decision,
        price,
        risk,
        smart_money
    ):

        data = json.loads(
            self.file.read_text()
        )


        trade = {
            "symbol": symbol,
            "decision": decision,
            "entry": price,
            "risk": risk,
            "smart_money": smart_money,
            "time": datetime.utcnow().isoformat()
        }


        data.append(trade)


        self.file.write_text(
            json.dumps(
                data,
                indent=4
            )
        )


        return trade



    def history(
        self
    ):

        return json.loads(
            self.file.read_text()
        )


trade_journal = TradeJournal()
