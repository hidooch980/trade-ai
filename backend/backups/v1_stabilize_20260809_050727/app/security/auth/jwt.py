from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from app.core_config import settings

def create_access_token(
    user_id: UUID,
    username: str,
    language: str = "en",
    role: str = "CUSTOMER",
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),
        "username": username,
        "language": language,
        "role": role,
        "iat": now,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
