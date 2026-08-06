import logging
import os


class TradeLogger:

    def __init__(self):

        os.makedirs(
            "logs",
            exist_ok=True
        )

        self.logger = logging.getLogger(
            "TRADE_AI"
        )

        self.logger.setLevel(
            logging.INFO
        )


        if not self.logger.handlers:

            handler = logging.FileHandler(
                "logs/trade_ai.log"
            )

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            handler.setFormatter(
                formatter
            )

            self.logger.addHandler(
                handler
            )


    def info(
        self,
        message
    ):

        self.logger.info(
            message
        )


    def error(
        self,
        message
    ):

        self.logger.error(
            message
        )
