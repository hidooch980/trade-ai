"""
Compatibility bridge for broker-layer imports.

The canonical MT5 implementation currently lives in:
app.market.bridge.mt5_bridge
"""

from app.market.bridge.mt5_bridge import MT5Bridge, mt5_bridge

__all__ = ["MT5Bridge", "mt5_bridge"]
