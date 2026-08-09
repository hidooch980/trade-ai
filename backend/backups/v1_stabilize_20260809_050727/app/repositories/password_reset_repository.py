from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.password_reset_token import PasswordResetToken


class PasswordResetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: UUID,
        token_hash: str,
        expires_at: datetime,
    ) -> PasswordResetToken:
        item = PasswordResetToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)

        return item

    async def get_by_hash(
        self,
        token_hash: str,
    ) -> PasswordResetToken | None:
        result = await self.session.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash == token_hash
            )
        )

        return result.scalar_one_or_none()

    async def invalidate_user_tokens(self, user_id: UUID) -> None:
        await self.session.execute(
            update(PasswordResetToken)
            .where(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.used_at.is_(None),
            )
            .values(
                used_at=datetime.now(timezone.utc)
            )
        )

        await self.session.flush()
