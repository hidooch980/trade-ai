class DashboardService:

    def __init__(
        self,
        performance_service
    ):
        self.performance_service = performance_service


    def get_dashboard(
        self,
        trades
    ):

        performance = (
            self.performance_service
            .summarize(trades)
        )


        return {

            "dashboard": {

                "performance": performance,

                "status": "ACTIVE"

            }

        }
