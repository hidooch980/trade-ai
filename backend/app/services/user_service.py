from enum import Enum
from typing import NamedTuple
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.security.password import hash_password, verify_password
from app.i18n.manager import normalize_language
from app.security.auth.brute_force import (
    is_account_locked,
    register_failed_login,
    reset_failed_logins,
)


class AuthOutcome(str, Enum):
    """Why an authentication attempt ended the way it did."""

    OK = "OK"
    UNKNOWN_USER = "UNKNOWN_USER"
    LOCKED = "LOCKED"
    BAD_PASSWORD = "BAD_PASSWORD"


class AuthAttempt(NamedTuple):
    outcome: AuthOutcome
    user: User | None = None

    @property
    def ok(self) -> bool:
        return self.outcome is AuthOutcome.OK


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)

    async def get_by_username(self, username: str) -> User | None:
        return await self.repository.get_by_username(username)

    async def create(
        self,
        email: str,
        username: str,
        password: str,
        language: str = "en",
    ) -> User:
        existing_email = await self.repository.get_by_email(email)

        if existing_email:
            raise ValueError(
                "User email already exists"
            )

        existing_username = await self.repository.get_by_username(
            username
        )

        if existing_username:
            raise ValueError(
                "Username already exists"
            )

        language = normalize_language(language)
        password_hash = hash_password(password)

        return await self.repository.create(
            email=email,
            username=username,
            password_hash=password_hash,
            language=language,
        )

    async def authenticate(
        self,
        username: str,
        password: str,
    ) -> AuthAttempt:
        """
        Reports *why* an attempt failed, not just that it did.

        Collapsing a locked account into the same answer as a wrong password
        leaves the caller unable to say so, and leaves the failure counter
        unreadable. The counter is mutated here but only reaches the database
        if the caller commits — a rejected login has to commit too, or the
        lockout threshold is never crossed.
        """
        user = await self.repository.get_by_username(username)

        if not user or not user.password_hash:
            return AuthAttempt(AuthOutcome.UNKNOWN_USER)

        if is_account_locked(user):
            return AuthAttempt(AuthOutcome.LOCKED, user)

        if not verify_password(
            password,
            user.password_hash,
        ):
            register_failed_login(user)
            return AuthAttempt(AuthOutcome.BAD_PASSWORD, user)

        reset_failed_logins(user)

        return AuthAttempt(AuthOutcome.OK, user)
