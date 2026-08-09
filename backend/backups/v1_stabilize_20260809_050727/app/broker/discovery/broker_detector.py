class BrokerDetector:
    """
    Detect broker connection capabilities from user/system supplied
    information. No credentials are searched or collected here.
    """

    CONNECTION_KEYWORDS = {
        "mt5": [
            "metatrader 5",
            "meta trader 5",
            "mt5",
        ],
        "mt4": [
            "metatrader 4",
            "meta trader 4",
            "mt4",
        ],
        "ctrader": [
            "ctrader",
            "c trader",
        ],
        "fix": [
            "fix api",
            "fix protocol",
            "fix 4.4",
            "fix 5.0",
        ],
        "rest": [
            "rest api",
            "rest",
            "http api",
        ],
        "websocket": [
            "websocket",
            "websocket api",
            "ws api",
        ],
    }

    def detect(self, text: str) -> dict:
        value = str(text or "").lower()

        matches = []

        for connection_type, keywords in self.CONNECTION_KEYWORDS.items():
            if any(keyword in value for keyword in keywords):
                matches.append(connection_type)

        return {
            "input": text,
            "connection_types": sorted(set(matches)),
            "detected": bool(matches),
        }


broker_detector = BrokerDetector()
