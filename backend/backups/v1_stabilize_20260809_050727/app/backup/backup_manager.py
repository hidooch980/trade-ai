import json
import os
from datetime import datetime


class BackupManager:

    def __init__(self):

        os.makedirs(
            "backups",
            exist_ok=True
        )


    def create_backup(
        self,
        name,
        data
    ):

        filename = (
            f"backups/{name}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )


        with open(
            filename,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                default=str
            )


        return {

            "created": True,

            "file": filename

        }


    def restore(
        self,
        filepath
    ):

        with open(
            filepath,
            "r"
        ) as file:

            return json.load(
                file
            )
