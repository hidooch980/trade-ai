from dataclasses import dataclass, field
from typing import Any


@dataclass
class BrokerProfile:
    name: str
    slug: str
    country: str | None = None
    website: str | None = None
    capabilities: list[str] = field(default_factory=list)
    connection_types: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities
