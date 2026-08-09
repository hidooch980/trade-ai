import hashlib
import time


class AuthManager:

    def __init__(self):
        self.users = {}


    def create_user(
        self,
        username,
        password,
        role="TRADER"
    ):

        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()

        self.users[username] = {
            "password": password_hash,
            "role": role
        }

        return {
            "created": True,
            "username": username,
            "role": role
        }


    def authenticate(
        self,
        username,
        password
    ):

        user = self.users.get(username)

        if not user:
            return {
                "authenticated": False
            }

        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()

        if password_hash != user["password"]:
            return {
                "authenticated": False
            }

        return {
            "authenticated": True,
            "username": username,
            "role": user["role"],
            "token": str(time.time())
        }
