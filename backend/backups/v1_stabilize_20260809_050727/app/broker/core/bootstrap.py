from app.broker.core.registry import broker_registry
from app.broker.adapters.simulator import SimulatorAdapter
from app.broker.adapters.mt5 import MT5Adapter


def register_builtin_brokers():
    broker_registry.register("simulator", SimulatorAdapter)
    broker_registry.register("simulation", SimulatorAdapter)
    broker_registry.register("mt5", MT5Adapter)
    broker_registry.register("metatrader5", MT5Adapter)
    return broker_registry.list()


registered_brokers = register_builtin_brokers()
