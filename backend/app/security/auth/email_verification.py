import hashlib
import secrets
from datetime import datetime, timedelta, timezone


EMAIL_VERIFICATION_EXPIRE_HOURS = 24


def generate_verification_token() -> str:
    return secrets.token_urlsafe(64)


def hash_verification_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def verification_token_expiry() -> datetime:
    return (
        datetime.now(timezone.utc)
        + timedelta(hours=EMAIL_VERIFICATION_EXPIRE_HOURS)
    )
