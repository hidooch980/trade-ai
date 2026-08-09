from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.auth_session import AuthSession

class AuthSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, refresh_token_hash: str, expires_at: datetime, device_name: str | None = None, ip_address: str | None = None, user_agent: str | None = None) -> AuthSession:
        item = AuthSession(
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def get_by_hash(self, token_hash: str) -> AuthSession | None:
        result = await self.session.execute(
            select(AuthSession).where(AuthSession.refresh_token_hash == token_hash)
        )
        return result.scalar_one_or_none()

    async def revoke(self, item: AuthSession) -> None:
        item.revoked_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        await self.session.execute(
            update(AuthSession)
            .where(
                AuthSession.user_id == user_id,
                AuthSession.revoked_at.is_(None),
            )
            .values(revoked_at=datetime.now(timezone.utc))
        )
        await self.session.flush()

    async def list_for_user(self, user_id: UUID) -> list[AuthSession]:
        result = await self.session.execute(
            select(AuthSession)
            .where(AuthSession.user_id == user_id)
            .order_by(AuthSession.created_at.desc())
        )
        return list(result.scalars().all())
