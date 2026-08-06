from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderStatus
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, session: AsyncSession):
        self.repository = OrderRepository(session)

    async def get_by_id(self, order_id: UUID) -> Order | None:
        return await self.repository.get_by_id(order_id)

    async def list_by_account(
        self,
        account_id: UUID,
        limit: int = 100,
    ) -> list[Order]:
        return await self.repository.list_by_account(
            account_id=account_id,
            limit=limit,
        )

    async def list_open_by_account(
        self,
        account_id: UUID,
    ) -> list[Order]:
        return await self.repository.list_open_by_account(account_id)

    async def create(
        self,
        account_id: UUID,
        symbol_id: UUID,
        side,
        order_type,
        quantity,
        price=None,
        stop_price=None,
    ) -> Order:
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than zero")

        if price is not None and price <= 0:
            raise ValueError("Order price must be greater than zero")

        if stop_price is not None and stop_price <= 0:
            raise ValueError("Stop price must be greater than zero")

        return await self.repository.create(
            account_id=account_id,
            symbol_id=symbol_id,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )

    async def update_status(
        self,
        order: Order,
        status: OrderStatus,
    ) -> Order:
        return await self.repository.update_status(order, status)
