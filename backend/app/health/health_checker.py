from datetime import datetime


class HealthChecker:

    def __init__(self):

        self.services = {}


    def register(
        self,
        name,
        status
    ):

        self.services[name] = status


    def check(self):

        failed = [

            name

            for name, status in self.services.items()

            if not status

        ]


        return {

            "system": "TRADE_AI",

            "time": datetime.now(),

            "status": "HEALTHY"
            if not failed else "DEGRADED",

            "services": self.services,

            "failed": failed

        }
