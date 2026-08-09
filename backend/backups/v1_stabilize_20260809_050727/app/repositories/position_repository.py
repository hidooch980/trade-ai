from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.position import Position


class PositionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        position_id: UUID,
    ) -> Position | None:
        result = await self.session.execute(
            select(Position).where(Position.id == position_id)
        )
        return result.scalar_one_or_none()

    async def list_by_account(
        self,
        account_id: UUID,
    ) -> list[Position]:
        result = await self.session.execute(
            select(Position)
            .where(Position.account_id == account_id)
            .order_by(Position.opened_at.desc())
        )
        return list(result.scalars().all())

    async def list_by_symbol(
        self,
        symbol_id: UUID,
    ) -> list[Position]:
        result = await self.session.execute(
            select(Position)
            .where(Position.symbol_id == symbol_id)
            .order_by(Position.opened_at.desc())
        )
        return list(result.scalars().all())
