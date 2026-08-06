class PermissionManager:

    def __init__(self):

        self.permissions = {

            "ADMIN": [

                "OPEN_TRADE",
                "CLOSE_TRADE",
                "VIEW_REPORTS",
                "MANAGE_USERS"

            ],

            "TRADER": [

                "OPEN_TRADE",
                "CLOSE_TRADE",
                "VIEW_REPORTS"

            ],

            "VIEWER": [

                "VIEW_REPORTS"

            ]

        }


    def check(

        self,
        role,
        action

    ):

        allowed = self.permissions.get(
            role,
            []
        )


        return {

            "role": role,

            "action": action,

            "allowed": action in allowed

        }
