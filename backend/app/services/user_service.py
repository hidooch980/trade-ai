from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)

    async def get_by_username(self, username: str) -> User | None:
        return await self.repository.get_by_username(username)

    async def create(self, email: str, username: str) -> User:
        existing_email = await self.repository.get_by_email(email)
        if existing_email:
            raise ValueError("User email already exists")

        existing_username = await self.repository.get_by_username(username)
        if existing_username:
            raise ValueError("Username already exists")

        return await self.repository.create(email=email, username=username)
