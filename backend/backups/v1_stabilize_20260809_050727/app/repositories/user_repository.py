from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        username: str,
        password_hash: str,
        language: str = "en",
    ) -> User:
        user = User(
            email=email,
            username=username,
            language=language,
            password_hash=password_hash,
        )

        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def update_password(
        self,
        user: User,
        password_hash: str,
    ) -> None:
        user.password_hash = password_hash
        user.failed_login_attempts = 0
        user.locked_until = None
        await self.session.flush()

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.flush()
