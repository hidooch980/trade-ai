from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# Kept in step with PermissionManager's role table plus the model's default.
ASSIGNABLE_ROLES = ("ADMIN", "TRADER", "VIEWER", "CUSTOMER")


class AdminUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    username: str
    language: str
    role: str
    failed_login_attempts: int
    locked_until: datetime | None
    is_locked: bool
    email_verified_at: datetime | None
    active_sessions: int
    created_at: datetime
    updated_at: datetime


class AdminUserListResponse(BaseModel):
    items: list[AdminUserResponse]
    total: int
    limit: int
    offset: int


class RoleUpdateRequest(BaseModel):
    role: str = Field(min_length=3, max_length=20)


class LockRequest(BaseModel):
    """Omit `minutes` to fall back to the standard lockout window."""

    minutes: int | None = Field(default=None, ge=1, le=60 * 24 * 30)
