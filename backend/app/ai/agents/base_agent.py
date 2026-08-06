from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def analyze(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def result(self, signal: str, confidence: float, reason: str):
        return {
            "agent": self.name,
            "signal": signal,
            "confidence": confidence,
            "reason": reason,
        }
