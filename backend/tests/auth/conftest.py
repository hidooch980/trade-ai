"""
Test harness for the auth router.

Runs against a real PostgreSQL instance because the models use
`postgresql.UUID` and `gen_random_uuid()` server defaults, which SQLite
cannot express. Point TEST_DATABASE_URL at any throwaway database.
"""

import os

import pytest
import pytest_asyncio

TEST_DATABASE_URL = os.environ.setdefault(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres@127.0.0.1:55432/trade_ai_test",
)
# app.db.session builds its engine from settings at import time.
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-not-a-real-key")

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.exceptions import RequestValidationError  # noqa: E402
from starlette.exceptions import HTTPException as StarletteHTTPException  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402
from sqlalchemy import text  # noqa: E402
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa: E402

import app.models  # noqa: F401,E402  — registers every table on Base.metadata
from app.api.routes import accounts as account_routes  # noqa: E402
from app.api.routes import admin_users as admin_routes  # noqa: E402
from app.api.routes import risk as risk_routes  # noqa: E402
from app.api.routes import auth as auth_routes  # noqa: E402
from app.db.session import Base, get_db  # noqa: E402
from app.i18n.errors import (  # noqa: E402
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.broker.security.credential_manager import credential_manager  # noqa: E402
from app.security.auth.rate_limit import auth_rate_limiter  # noqa: E402

TABLES = (
    "auth_sessions",
    "password_reset_tokens",
    "email_verification_tokens",
    "account_risk_policies",
    "trading_accounts",
    "users",
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="session")
async def engine():
    eng = create_async_engine(TEST_DATABASE_URL, future=True)
    async with eng.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
        # Rebuild from scratch so a model change is picked up rather than
        # silently running against last session's columns.
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()


@pytest_asyncio.fixture
async def session_factory(engine):
    async with engine.begin() as conn:
        # TRUNCATE rather than drop: far quicker between tests, and CASCADE
        # keeps the tables that reference users consistent.
        await conn.execute(
            text(f"TRUNCATE {', '.join(TABLES)} RESTART IDENTITY CASCADE")
        )
    # Both of these are process-global; leftovers would bleed between tests.
    auth_rate_limiter._attempts.clear()
    credential_manager.clear()
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def client(session_factory):
    api = FastAPI()
    # Same error handling as app/api/main.py, so tests see the real response
    # bodies rather than FastAPI's defaults.
    api.add_exception_handler(StarletteHTTPException, http_exception_handler)
    api.add_exception_handler(HTTPException, http_exception_handler)
    api.add_exception_handler(RequestValidationError, validation_exception_handler)
    api.add_exception_handler(Exception, general_exception_handler)
    api.include_router(auth_routes.router)
    api.include_router(admin_routes.router)
    api.include_router(account_routes.router)
    api.include_router(risk_routes.router)

    async def override_get_db():
        async with session_factory() as session:
            yield session

    api.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=api)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c


@pytest_asyncio.fixture
async def db(session_factory):
    """A session for asserting directly against the database."""
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def account(client):
    """A registered user plus the credentials used to create it."""
    creds = {
        "email": "trader@example.com",
        "username": "trader",
        "password": "correct-horse-battery",
    }
    res = await client.post("/auth/register", json=creds)
    assert res.status_code == 201, res.text
    return {**creds, "id": res.json()["id"]}


@pytest_asyncio.fixture
async def admin(client, db):
    """A registered user promoted to ADMIN, with a bearer token."""
    from sqlalchemy import select

    from app.models.user import User

    creds = {
        "email": "boss@example.com",
        "username": "boss",
        "password": "boss-password-9000",
    }
    res = await client.post("/auth/register", json=creds)
    assert res.status_code == 201, res.text

    user = (
        await db.execute(select(User).where(User.username == creds["username"]))
    ).scalar_one()
    user.role = "ADMIN"
    await db.commit()

    login = await client.post(
        "/auth/login",
        json={"username": creds["username"], "password": creds["password"]},
    )
    assert login.status_code == 200, login.text

    return {
        **creds,
        "id": login.json()["user"]["id"],
        "headers": {"Authorization": f"Bearer {login.json()['access_token']}"},
    }


@pytest_asyncio.fixture
async def member_token(client, account):
    """A bearer token for the ordinary (non-admin) account."""
    res = await client.post(
        "/auth/login",
        json={"username": account["username"], "password": account["password"]},
    )
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


@pytest_asyncio.fixture
async def member_headers(member_token):
    return member_token


@pytest_asyncio.fixture
async def second_account(client):
    """A second ordinary user, for proving cross-user isolation."""
    creds = {
        "email": "other@example.com",
        "username": "other",
        "password": "another-good-password",
    }
    res = await client.post("/auth/register", json=creds)
    assert res.status_code == 201, res.text

    login = await client.post(
        "/auth/login",
        json={"username": creds["username"], "password": creds["password"]},
    )
    assert login.status_code == 200, login.text

    return {
        **creds,
        "id": login.json()["user"]["id"],
        "headers": {"Authorization": f"Bearer {login.json()['access_token']}"},
    }
