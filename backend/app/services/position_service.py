from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.position import Position
from app.repositories.position_repository import PositionRepository


class PositionService:
    def __init__(self, session: AsyncSession):
        self.repository = PositionRepository(session)

    async def get_by_id(self, position_id: UUID) -> Position | None:
        return await self.repository.get_by_id(position_id)

    async def list_by_account(self, account_id: UUID) -> list[Position]:
        return await self.repository.list_by_account(account_id)

    async def list_by_symbol(self, symbol_id: UUID) -> list[Position]:
        return await self.repository.list_by_symbol(symbol_id)
