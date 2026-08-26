"""
User administration.

Read and moderation routes over the users table, gated on the MANAGE_USERS
permission. Nothing here can read or set a password — resetting one still
goes through the owner's own /auth/forgot-password flow.
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.repositories.auth_session_repository import AuthSessionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin import (
    ASSIGNABLE_ROLES,
    AdminUserListResponse,
    AdminUserResponse,
    LockRequest,
    RoleUpdateRequest,
)
from app.schemas.auth import SessionResponse
from app.security.auth.brute_force import LOCKOUT_MINUTES
from app.security.auth.dependencies import require_admin

router = APIRouter(prefix="/admin/users", tags=["admin"])


def present(user: User, active_sessions: int) -> AdminUserResponse:
    now = datetime.now(timezone.utc)

    return AdminUserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        language=user.language,
        role=user.role,
        failed_login_attempts=user.failed_login_attempts,
        locked_until=user.locked_until,
        is_locked=user.locked_until is not None and user.locked_until > now,
        email_verified_at=user.email_verified_at,
        active_sessions=active_sessions,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


async def commit_and_present(
    db: AsyncSession,
    repository: UserRepository,
    user: User,
) -> AdminUserResponse:
    """
    `updated_at` carries an onupdate default, so committing an UPDATE expires
    it. Re-read the row here rather than letting serialisation lazy-load the
    attribute, which would be blocking IO outside the async context.
    """
    await db.commit()
    await db.refresh(user)

    return present(user, await repository.count_active_sessions(user.id))


async def load(db: AsyncSession, user_id: UUID) -> User:
    user = await UserRepository(db).get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.get("", response_model=AdminUserListResponse)
async def list_users(
    search: str | None = Query(default=None, max_length=255),
    role: str | None = Query(default=None, max_length=20),
    locked: bool | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    _admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    rows, total = await UserRepository(db).list_users(
        search=search,
        role=role,
        locked=locked,
        limit=limit,
        offset=offset,
    )

    return AdminUserListResponse(
        items=[present(user, count) for user, count in rows],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{user_id}", response_model=AdminUserResponse)
async def get_user(
    user_id: UUID,
    _admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    user = await load(db, user_id)
    active = await UserRepository(db).count_active_sessions(user.id)

    return present(user, active)


@router.get("/{user_id}/sessions", response_model=list[SessionResponse])
async def user_sessions(
    user_id: UUID,
    _admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    await load(db, user_id)

    return await AuthSessionRepository(db).list_for_user(user_id)


@router.patch("/{user_id}/role", response_model=AdminUserResponse)
async def set_role(
    user_id: UUID,
    data: RoleUpdateRequest,
    admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    role = data.role.upper()

    if role not in ASSIGNABLE_ROLES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Role must be one of: {', '.join(ASSIGNABLE_ROLES)}",
        )

    if admin.id == user_id:
        # Demoting yourself would take the last admin out with it.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot change your own role",
        )

    repository = UserRepository(db)
    user = await load(db, user_id)

    await repository.set_role(user, role)

    return await commit_and_present(db, repository, user)


@router.post("/{user_id}/lock", response_model=AdminUserResponse)
async def lock_user(
    user_id: UUID,
    data: LockRequest,
    admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    if admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot lock your own account",
        )

    repository = UserRepository(db)
    user = await load(db, user_id)

    minutes = data.minutes or LOCKOUT_MINUTES
    until = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    await repository.set_lock(user, until)
    # A lock that leaves live sessions running is not a lock.
    await AuthSessionRepository(db).revoke_all_for_user(user.id)

    return await commit_and_present(db, repository, user)


@router.post("/{user_id}/unlock", response_model=AdminUserResponse)
async def unlock_user(
    user_id: UUID,
    _admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    repository = UserRepository(db)
    user = await load(db, user_id)

    await repository.set_lock(user, None)

    return await commit_and_present(db, repository, user)


@router.post("/{user_id}/revoke-sessions", response_model=AdminUserResponse)
async def revoke_sessions(
    user_id: UUID,
    _admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    repository = UserRepository(db)
    user = await load(db, user_id)

    await AuthSessionRepository(db).revoke_all_for_user(user.id)

    return await commit_and_present(db, repository, user)
