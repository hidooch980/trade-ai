from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderStatus


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        order_id: UUID,
    ) -> Order | None:
        result = await self.session.execute(
            select(Order).where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def list_by_account(
        self,
        account_id: UUID,
        limit: int = 100,
    ) -> list[Order]:
        result = await self.session.execute(
            select(Order)
            .where(Order.account_id == account_id)
            .order_by(Order.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def list_open_by_account(
        self,
        account_id: UUID,
    ) -> list[Order]:
        result = await self.session.execute(
            select(Order)
            .where(
                Order.account_id == account_id,
                Order.status.in_(
                    [
                        OrderStatus.PENDING,
                        OrderStatus.OPEN,
                        OrderStatus.PARTIALLY_FILLED,
                    ]
                ),
            )
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

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
        order = Order(
            account_id=account_id,
            symbol_id=symbol_id,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )

        self.session.add(order)
        await self.session.flush()
        await self.session.refresh(order)

        return order

    async def update_status(
        self,
        order: Order,
        status: OrderStatus,
    ) -> Order:
        order.status = status

        await self.session.flush()
        await self.session.refresh(order)

        return order
