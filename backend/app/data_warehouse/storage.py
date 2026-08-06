import json
from pathlib import Path


class AIDataWarehouse:

    def __init__(self):
        self.storage=Path(
            "data/warehouse.json"
        )


    def load(self):

        if self.storage.exists():
            return json.loads(
                self.storage.read_text()
            )

        return []


    def save(self,record):

        data=self.load()

        data.append(record)

        self.storage.parent.mkdir(
            exist_ok=True
        )

        self.storage.write_text(
            json.dumps(
                data,
                indent=2
            )
        )

        return record


    def query(self):

        return self.load()


    def stats(self):

        return {
            "records":len(self.load()),
            "system":"ACTIVE"
        }


data_warehouse=AIDataWarehouse()
