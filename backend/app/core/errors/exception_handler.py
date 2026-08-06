from app.core.logging.logger import TradeLogger


class ExceptionHandler:

    def __init__(self):

        self.logger = TradeLogger()


    def handle(
        self,
        error,
        context="SYSTEM"
    ):

        message = (
            f"{context} ERROR: {str(error)}"
        )

        self.logger.error(
            message
        )


        return {

            "status": "ERROR",

            "context": context,

            "message": str(error),

            "recovered": True

        }
