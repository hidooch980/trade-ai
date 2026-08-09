class APIGateway:
    """
    Application/API gateway facade.

    Keeps compatibility with the monitoring/dashboard API used by
    tests and higher-level application code.
    """

    def __init__(self, monitor=None, dashboard=None):
        self.monitor = monitor
        self.dashboard = dashboard

        # Preserve the existing developer-key/request functionality.
        self.keys = {}
        self.requests = []

    def create_key(self, developer):
        key = {
            "developer": developer,
            "status": "ACTIVE",
        }

        self.keys[developer] = key
        return key

    def request(self, developer, service):
        req = {
            "developer": developer,
            "service": service,
            "status": "RECEIVED",
        }

        self.requests.append(req)
        return req

    def check_permission(self, developer):
        return {
            "developer": developer,
            "permission": "VERIFIED",
        }

    def health(self):
        if self.monitor is not None:
            try:
                if hasattr(self.monitor, "status"):
                    return self.monitor.status()
            except Exception:
                pass

        return {
            "gateway": "ONLINE",
            "monitor": "ONLINE" if self.monitor is not None else "NOT_CONFIGURED",
        }

    def system_status(self):
        return {
            "gateway": "ONLINE",
            "monitor": "CONNECTED" if self.monitor is not None else "NOT_CONFIGURED",
            "dashboard": "CONNECTED" if self.dashboard is not None else "NOT_CONFIGURED",
            "keys": len(self.keys),
            "requests": len(self.requests),
        }

    def dashboard_data(self, trades):
        if self.dashboard is not None:
            # Support common dashboard service APIs without coupling
            # the gateway to one exact implementation.
            for method_name in (
                "calculate",
                "generate",
                "get_dashboard",
                "dashboard_data",
                "analyze",
            ):
                method = getattr(self.dashboard, method_name, None)
                if callable(method):
                    try:
                        return method(trades)
                    except TypeError:
                        continue

        return {
            "trades": trades,
            "count": len(trades),
        }

    def status(self):
        return {
            "keys": len(self.keys),
            "requests": len(self.requests),
            "gateway": "ONLINE",
        }


# Backward compatibility with the previous class name.
AIAPIGateway = APIGateway

api_gateway = APIGateway()
