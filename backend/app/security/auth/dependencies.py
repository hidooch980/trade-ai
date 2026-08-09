from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.security.auth.jwt import decode_access_token
from app.services.user_service import UserService
from app.i18n.manager import i18n, normalize_language

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=i18n.translate("error.unauthorized"),
        )

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = UUID(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=i18n.translate("error.unauthorized"),
        )

    user = await UserService(db).get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=i18n.translate("auth.user_not_found"),
        )

    i18n.set_language(normalize_language(user.language))
    return user
