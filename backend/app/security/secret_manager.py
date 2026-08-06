import os


class SecretManager:

    def get_secret(
        self,
        key
    ):

        value = os.getenv(key)

        if not value:
            return {
                "available": False,
                "key": key
            }

        return {
            "available": True,
            "key": key,
            "value": value
        }


    def has_secret(
        self,
        key
    ):

        return bool(
            os.getenv(key)
        )
