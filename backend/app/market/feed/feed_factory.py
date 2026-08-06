from .simulation_feed import SimulationFeed
from .mt5_feed import MT5Feed
from .config import FEED_MODE


class FeedFactory:

    @staticmethod
    def create(mode=None):

        mode = mode or FEED_MODE

        if mode == "SIMULATION":
            return SimulationFeed()

        if mode == "MT5":
            return MT5Feed()

        raise ValueError(f"Unsupported feed mode: {mode}")


feed_factory = FeedFactory()
