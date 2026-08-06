class APIGateway:

    def __init__(
        self,
        monitor,
        dashboard
    ):

        self.monitor = monitor
        self.dashboard = dashboard


    def health(self):

        return {

            "status": "ONLINE",

            "service": "TRADE_AI_API"

        }


    def system_status(self):

        return {

            "health": self.health(),

            "monitor": self.monitor.status()

        }


    def dashboard_data(
        self,
        trades
    ):

        return self.dashboard.get_dashboard(
            trades
        )
