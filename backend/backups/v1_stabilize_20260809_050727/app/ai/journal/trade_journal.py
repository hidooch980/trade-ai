import json
import os
from pathlib import Path
from datetime import datetime


class TradeJournal:
    def __init__(self):
        self.file = Path("data/trade_journal.json")
        self.jsonl_file = Path("data/trade_journal.jsonl")

        self.file.parent.mkdir(exist_ok=True)

        if not self.file.exists():
            self.file.write_text("[]", encoding="utf-8")

        self.jsonl_file.touch(exist_ok=True)

    def _append_jsonl(self, record):
        payload = json.dumps(
            record,
            ensure_ascii=False,
            separators=(",", ":")
        ) + "\n"

        with self.jsonl_file.open("a", encoding="utf-8") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())

    def _read_jsonl(self):
        if not self.jsonl_file.exists():
            return []

        records = []

        with self.jsonl_file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return records

    def history(self, limit=None):
        records = self._read_jsonl()

        if limit is not None:
            try:
                limit = max(0, int(limit))
            except (TypeError, ValueError):
                limit = None

            if limit is not None:
                if limit == 0:
                    return []
                return records[-limit:]

        return records

    def all(self, limit=None):
        return self.history(limit=limit)

    def replace_history(self, trades):
        if not isinstance(trades, list):
            raise ValueError("TRADE_HISTORY_MUST_BE_LIST")

        tmp = self.file.with_suffix(".json.tmp")

        payload = json.dumps(
            trades,
            indent=4,
            ensure_ascii=False
        )

        with tmp.open("w", encoding="utf-8") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())

        os.replace(tmp, self.file)

        # replace_history means the complete history is authoritative.
        # New JSONL records must therefore be cleared.
        with self.jsonl_file.open("w", encoding="utf-8") as f:
            f.flush()
            os.fsync(f.fileno())

        return trades

    def record(
        self,
        symbol,
        decision,
        price,
        risk,
        smart_money
    ):
        trade = {
            "symbol": symbol,
            "decision": decision,
            "entry": price,
            "risk": risk,
            "smart_money": smart_money,
            "time": datetime.utcnow().isoformat()
        }

        self._append_jsonl(trade)
        return trade

    def add(self, event, data):
        record = {
            "event": event,
            "data": data,
            "time": datetime.utcnow().isoformat()
        }

        self._append_jsonl(record)
        return record

    def record_closed(
        self,
        symbol,
        decision,
        entry_price,
        exit_price,
        volume,
        pnl
    ):
        trade = {
            "symbol": symbol,
            "decision": decision,
            "entry": entry_price,
            "exit": exit_price,
            "volume": volume,
            "profit": pnl,
            "status": "CLOSED",
            "time": datetime.utcnow().isoformat()
        }

        self._append_jsonl(trade)
        return trade


trade_journal = TradeJournal()
