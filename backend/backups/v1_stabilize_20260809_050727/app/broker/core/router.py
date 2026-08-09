from app.broker.core.bootstrap import register_builtin_brokers
from app.broker.core.registry import broker_registry


class BrokerRouter:
    def __init__(self):
        register_builtin_brokers()

    def available(self):
        return broker_registry.list()

    def resolve(self, broker_name):
        if broker_registry.exists(broker_name):
            return broker_registry.get(broker_name)

        aliases = {
            "meta trader 5": "mt5",
            "metatrader 5": "mt5",
            "meta_trader_5": "mt5",
            "mt5": "mt5",
            "sim": "simulator",
            "simulation": "simulator",
        }

        key = aliases.get(
            str(broker_name or "").strip().lower(),
            str(broker_name or "").strip().lower(),
        )

        return broker_registry.get(key)

    def create(self, broker_name, *args, **kwargs):
        adapter_cls = self.resolve(broker_name)

        if adapter_cls is None:
            raise KeyError(
                f"Broker not registered: {broker_name}. "
                f"Available: {self.available()}"
            )

        return adapter_cls(*args, **kwargs)


broker_router = BrokerRouter()
