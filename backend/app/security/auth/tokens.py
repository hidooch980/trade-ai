import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.core_config import settings
from app.security.auth.jwt import create_access_token


REFRESH_TOKEN_EXPIRE_DAYS = 30


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def refresh_token_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )


def create_auth_tokens(
    user_id: UUID,
    username: str,
    language: str,
) -> tuple[str, str, datetime]:
    access_token = create_access_token(
        user_id=user_id,
        username=username,
        language=language,
    )

    refresh_token = create_refresh_token()
    expires_at = refresh_token_expiry()

    return access_token, refresh_token, expires_at
