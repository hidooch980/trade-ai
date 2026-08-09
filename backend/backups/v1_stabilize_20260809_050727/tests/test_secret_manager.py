import os

from app.security.secret_manager import SecretManager


os.environ["BROKER_API_KEY"] = "TEST_KEY_123"


manager = SecretManager()


result = manager.get_secret(
    "BROKER_API_KEY"
)


missing = manager.get_secret(
    "UNKNOWN_KEY"
)


print("AVAILABLE SECRET:")
print(result)

print()

print("MISSING SECRET:")
print(missing)

print()

print("HAS SECRET:")
print(
    manager.has_secret(
        "BROKER_API_KEY"
    )
)
