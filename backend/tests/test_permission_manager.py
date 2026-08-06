from app.security.permissions.permission_manager import PermissionManager


manager = PermissionManager()


admin_trade = manager.check(
    "ADMIN",
    "OPEN_TRADE"
)


viewer_trade = manager.check(
    "VIEWER",
    "OPEN_TRADE"
)


trader_report = manager.check(
    "TRADER",
    "VIEW_REPORTS"
)


print("ADMIN OPEN TRADE:")
print(admin_trade)

print()

print("VIEWER OPEN TRADE:")
print(viewer_trade)

print()

print("TRADER VIEW REPORTS:")
print(trader_report)
