from app.security.auth.auth_manager import AuthManager


auth = AuthManager()


created = auth.create_user(
    "trader",
    "secure123",
    "ADMIN"
)


login_success = auth.authenticate(
    "trader",
    "secure123"
)


login_failed = auth.authenticate(
    "trader",
    "wrong_password"
)


print("CREATE USER:")
print(created)

print()

print("LOGIN SUCCESS:")
print(login_success)

print()

print("LOGIN FAILED:")
print(login_failed)
