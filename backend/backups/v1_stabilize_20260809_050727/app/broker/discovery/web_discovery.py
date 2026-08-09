from __future__ import annotations

from dataclasses import asdict

from app.broker.core.broker_profile import BrokerProfile
from app.broker.core.router import broker_router


class BrokerWebDiscovery:
    """
    Safe public broker discovery.

    Never searches for or collects:
    - passwords
    - API secrets
    - tokens
    - private keys
    - account credentials
    """

    KNOWN_BROKERS = {
        "ic_markets": {
            "name": "IC Markets",
            "country": "Australia",
            "website": "https://www.icmarkets.com",
            "connection_types": ["mt4", "mt5", "ctrader"],
            "capabilities": ["forex", "indices", "commodities", "crypto", "cfds"],
        },
        "pepperstone": {
            "name": "Pepperstone",
            "country": "Australia",
            "website": "https://pepperstone.com",
            "connection_types": ["mt4", "mt5", "ctrader"],
            "capabilities": ["forex", "indices", "commodities", "crypto", "cfds"],
        },
        "xm": {
            "name": "XM",
            "country": "Cyprus",
            "website": "https://www.xm.com",
            "connection_types": ["mt4", "mt5"],
            "capabilities": ["forex", "indices", "commodities", "crypto", "cfds"],
        },
        "fxpro": {
            "name": "FxPro",
            "country": "United Kingdom",
            "website": "https://www.fxpro.com",
            "connection_types": ["mt4", "mt5", "ctrader"],
            "capabilities": ["forex", "indices", "commodities", "crypto", "cfds"],
        },
        "oanda": {
            "name": "OANDA",
            "country": "United States",
            "website": "https://www.oanda.com",
            "connection_types": ["rest", "websocket", "mt4", "mt5"],
            "capabilities": ["forex", "indices", "commodities", "cfds"],
        },
        "interactive_brokers": {
            "name": "Interactive Brokers",
            "country": "United States",
            "website": "https://www.interactivebrokers.com",
            "connection_types": ["rest", "websocket", "fix"],
            "capabilities": [
                "stocks",
                "options",
                "futures",
                "forex",
                "bonds",
                "etfs",
            ],
        },
        "ig": {
            "name": "IG",
            "country": "United Kingdom",
            "website": "https://www.ig.com",
            "connection_types": ["rest", "websocket", "mt4"],
            "capabilities": [
                "forex",
                "indices",
                "shares",
                "commodities",
                "crypto",
                "cfds",
            ],
        },
        "saxo": {
            "name": "Saxo",
            "country": "Denmark",
            "website": "https://www.home.saxo",
            "connection_types": ["rest", "websocket"],
            "capabilities": [
                "stocks",
                "etfs",
                "bonds",
                "forex",
                "options",
                "futures",
            ],
        },
        "tradestation": {
            "name": "TradeStation",
            "country": "United States",
            "website": "https://www.tradestation.com",
            "connection_types": ["rest", "websocket"],
            "capabilities": ["stocks", "options", "futures", "crypto"],
        },
        "alpaca": {
            "name": "Alpaca",
            "country": "United States",
            "website": "https://alpaca.markets",
            "connection_types": ["rest", "websocket"],
            "capabilities": ["stocks", "options", "crypto"],
        },
        "binance": {
            "name": "Binance",
            "country": "Global",
            "website": "https://www.binance.com",
            "connection_types": ["rest", "websocket"],
            "capabilities": ["crypto", "spot", "futures"],
        },
        "coinbase": {
            "name": "Coinbase",
            "country": "United States",
            "website": "https://www.coinbase.com",
            "connection_types": ["rest", "websocket"],
            "capabilities": ["crypto", "spot"],
        },
        "kraken": {
            "name": "Kraken",
            "country": "United States",
            "website": "https://www.kraken.com",
            "connection_types": ["rest", "websocket"],
            "capabilities": ["crypto", "spot", "futures"],
        },
    }

    ALIASES = {
        "icmarkets": "ic_markets",
        "ic markets": "ic_markets",
        "pepper stone": "pepperstone",
        "interactive brokers": "interactive_brokers",
        "ibkr": "interactive_brokers",
        "ig markets": "ig",
        "saxo bank": "saxo",
        "trade station": "tradestation",
    }

    def _normalize(self, value: str) -> str:
        value = str(value or "").strip().lower()
        value = value.replace("-", "_")
        value = value.replace(" ", "_")
        return value

    def _find_known(self, query: str):
        normalized = self._normalize(query)

        if normalized in self.KNOWN_BROKERS:
            return normalized

        alias_key = str(query or "").strip().lower()

        if alias_key in self.ALIASES:
            return self.ALIASES[alias_key]

        for slug, data in self.KNOWN_BROKERS.items():
            name = self._normalize(data["name"])

            if normalized == name:
                return slug

            if normalized in name or name in normalized:
                return slug

        return None

    async def discover(self, query: str) -> dict:
        query = str(query or "").strip()

        if not query:
            return {
                "success": False,
                "query": query,
                "reason": "EMPTY_QUERY",
                "profiles": [],
            }

        # First trust locally registered broker adapters.
        # This prevents known internal adapters such as MT5 from
        # being blocked by the public broker catalog.
        direct_adapter = broker_router.resolve(query)

        if direct_adapter is not None:
            return {
                "success": True,
                "query": query,
                "source": "local_adapter_registry",
                "profile": {
                    "name": query,
                    "slug": str(query).strip().lower().replace(" ", "_"),
                    "country": None,
                    "website": None,
                    "capabilities": [],
                    "connection_types": ["mt5"] if "meta" in query.lower() or "mt5" in query.lower() else [],
                    "metadata": {
                        "source": "local_adapter_registry",
                        "discovery": "broker_web_discovery",
                    },
                },
                "adapter_matches": [
                    {
                        "connection_type": "mt5" if "meta" in query.lower() or "mt5" in query.lower() else "direct",
                        "registered": True,
                        "adapter": direct_adapter.__name__,
                    }
                ],
                "ready_for_connection": True,
                "credentials_required": True,
                "credentials_found": False,
            }

        known_slug = self._find_known(query)

        if not known_slug:
            return {
                "success": False,
                "query": query,
                "source": "external_discovery_required",
                "profile": None,
                "adapter_matches": [],
                "ready_for_connection": False,
                "credentials_required": True,
                "credentials_found": False,
                "reason": "BROKER_NOT_IN_CATALOG",
            }

        data = self.KNOWN_BROKERS[known_slug]

        profile = BrokerProfile(
            name=data["name"],
            slug=known_slug,
            country=data.get("country"),
            website=data.get("website"),
            capabilities=data.get("capabilities", []),
            connection_types=data.get("connection_types", []),
            metadata={
                "source": "builtin_public_catalog",
                "discovery": "broker_web_discovery",
            },
        )

        adapters = []

        for connection_type in profile.connection_types:
            adapter = broker_router.resolve(connection_type)

            adapters.append(
                {
                    "connection_type": connection_type,
                    "registered": adapter is not None,
                    "adapter": adapter.__name__ if adapter else None,
                }
            )

        return {
            "success": True,
            "query": query,
            "source": "builtin_public_catalog",
            "profile": asdict(profile),
            "adapter_matches": adapters,
            "ready_for_connection": any(
                item["registered"] for item in adapters
            ),
            "credentials_required": True,
            "credentials_found": False,
        }


broker_web_discovery = BrokerWebDiscovery()
