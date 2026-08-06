import os

from app.backup.backup_manager import BackupManager


class RecoveryManager:

    def __init__(self):

        self.backup = BackupManager()


    def list_backups(self):

        if not os.path.exists(
            "backups"
        ):

            return []


        return [

            f"backups/{file}"

            for file in os.listdir(
                "backups"
            )

            if file.endswith(".json")

        ]


    def recover(
        self,
        filepath
    ):

        data = self.backup.restore(
            filepath
        )


        return {

            "status": "RECOVERED",

            "source": filepath,

            "data": data

        }
