from typing import Type


class BrokerRegistry:
    """
    Runtime registry for broker adapters.
    Adapters can be registered without changing trading logic.
    """

    def __init__(self):
        self._adapters: dict[str, Type] = {}

    def register(self, name: str, adapter_cls: Type):
        key = self._normalize(name)
        self._adapters[key] = adapter_cls
        return adapter_cls

    def get(self, name: str):
        return self._adapters.get(self._normalize(name))

    def create(self, name: str, *args, **kwargs):
        adapter_cls = self.get(name)

        if adapter_cls is None:
            raise KeyError(f"Broker adapter not registered: {name}")

        return adapter_cls(*args, **kwargs)

    def exists(self, name: str) -> bool:
        return self._normalize(name) in self._adapters

    def list(self):
        return sorted(self._adapters.keys())

    @staticmethod
    def _normalize(name: str) -> str:
        return str(name).strip().lower().replace(" ", "_")


broker_registry = BrokerRegistry()
