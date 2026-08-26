from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth_session import AuthSession
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

    async def list_users(
        self,
        *,
        search: str | None = None,
        role: str | None = None,
        locked: bool | None = None,
        limit: int = 25,
        offset: int = 0,
    ) -> tuple[list[tuple[User, int]], int]:
        """
        A page of users with each one's live session count, plus the total
        matching the same filters so the caller can paginate.
        """
        now = datetime.now(timezone.utc)

        conditions = []

        if search:
            needle = f"%{search.strip()}%"
            conditions.append(
                or_(User.email.ilike(needle), User.username.ilike(needle))
            )

        if role:
            conditions.append(User.role == role)

        if locked is True:
            conditions.append(User.locked_until.is_not(None))
            conditions.append(User.locked_until > now)
        elif locked is False:
            conditions.append(
                or_(User.locked_until.is_(None), User.locked_until <= now)
            )

        active_sessions = (
            select(func.count(AuthSession.id))
            .where(
                AuthSession.user_id == User.id,
                AuthSession.revoked_at.is_(None),
                AuthSession.expires_at > now,
            )
            .correlate(User)
            .scalar_subquery()
        )

        page = await self.session.execute(
            select(User, active_sessions)
            .where(*conditions)
            .order_by(User.created_at.desc(), User.id)
            .limit(limit)
            .offset(offset)
        )

        total = await self.session.execute(
            select(func.count()).select_from(User).where(*conditions)
        )

        return [(row[0], row[1]) for row in page.all()], total.scalar_one()

    async def count_active_sessions(self, user_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count(AuthSession.id)).where(
                AuthSession.user_id == user_id,
                AuthSession.revoked_at.is_(None),
                AuthSession.expires_at > datetime.now(timezone.utc),
            )
        )
        return result.scalar_one()

    async def set_role(self, user: User, role: str) -> None:
        user.role = role
        await self.session.flush()

    async def set_lock(self, user: User, until: datetime | None) -> None:
        user.locked_until = until

        if until is None:
            user.failed_login_attempts = 0

        await self.session.flush()

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
