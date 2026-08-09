import json
import os
import tempfile
from datetime import datetime, timezone


class MarketMemory:
    MAX_ACTIVE_RECORDS = 10000
    ROTATE_KEEP_RECORDS = 5000

    def __init__(self):
        self.legacy_file = "app/learning/data/market_memory.json"
        self.file = "app/learning/data/market_memory.jsonl"

        directory = os.path.dirname(self.file)
        os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.file) or self._is_empty_or_invalid_jsonl():
            self._migrate_legacy()


    def _is_empty_or_invalid_jsonl(self):
        try:
            if os.path.getsize(self.file) == 0:
                return True

            with open(self.file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            if not lines:
                return True

            for line in lines[:5]:
                json.loads(line)

            return False

        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return True

    def _migrate_legacy(self):
        if not os.path.exists(self.legacy_file):
            open(self.file, "a", encoding="utf-8").close()
            return

        try:
            with open(self.legacy_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                data = [data] if isinstance(data, dict) else []

        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Preserve the full old file as archive.
        archive = (
            self.legacy_file
            + ".archive_"
            + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        )

        try:
            os.replace(self.legacy_file, archive)
        except FileNotFoundError:
            pass

        active = data[-self.MAX_ACTIVE_RECORDS:]

        with open(self.file, "w", encoding="utf-8") as f:
            for record in active:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def _read_history(self):
        history = []

        try:
            with open(self.file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        record = json.loads(line)
                        history.append(record)
                    except json.JSONDecodeError:
                        continue

        except FileNotFoundError:
            return []

        return history[-self.MAX_ACTIVE_RECORDS:]

    def _append(self, record):
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def _rotate_if_needed(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return

        if len(lines) <= self.MAX_ACTIVE_RECORDS:
            return

        lines = lines[-self.ROTATE_KEEP_RECORDS:]

        directory = os.path.dirname(self.file)

        fd, tmp = tempfile.mkstemp(
            dir=directory,
            prefix=".market_memory_",
            suffix=".tmp",
            text=True,
        )

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.writelines(lines)
                f.flush()
                os.fsync(f.fileno())

            os.replace(tmp, self.file)

        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)

    def save(self, data):
        record = {
            "time": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }

        self._append(record)
        self._rotate_if_needed()

        return True

    def add(self, data):
        return self.save(data)

    def status(self):
        history = self.get_history()

        return {
            "records": len(history),
            "memory_file": self.file,
            "status": "ONLINE",
        }

    def get_history(self):
        return self._read_history()


market_memory = MarketMemory()
