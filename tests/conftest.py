import asyncio
import os
from typing import AsyncGenerator

import asyncpg
import pytest
import redis
from httpx import AsyncClient
from pydantic import EmailStr
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker

from src.auth.jwt import create_access_token
from src.config import setting

from starlette.testclient import TestClient
from src.main import app
from src.database import get_session, get_redis_connection, cleanup_redis_connection
from src.models import Base, User
from src.auth.security import get_password_hash

engine_test = create_async_engine(setting.TEST_DB_URL, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def override_get_redis_connection():
    redis_conn = redis.Redis(host="localhost", port=6378)
    yield redis_conn
    redis_conn.close()


app.dependency_overrides[get_session] = override_get_async_session
app.dependency_overrides[get_redis_connection] = override_get_redis_connection


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(setting.TEST_DB_URL.split("+asyncpg")))
    yield pool
    await pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_email(email: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                """SELECT * FROM users WHERE email = $1;""", email
            )

    return get_user_from_database_by_email


@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        id: int,
        email: EmailStr,
        username: str,
        hashed_password: str,
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO users VALUES ($1, $2, $3, $4)""",
                id,
                email,
                username,
                hashed_password,
            )

    return create_user_in_database


def create_test_auth_headers_for_user(id: int) -> dict[str, str]:
    user = {
        "id": id,
        "email": "test@example.com",
        "username": "test",
        "hashed_password": get_password_hash("testpass1"),
        "full_name": None,
        "location": None,
        "company": None,
    }
    access_token = create_access_token(User(**user))
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        id: int,
        email: EmailStr,
        username: str,
        hashed_password: str,
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO users VALUES ($1, $2, $3, $4)""",
                id,
                email,
                username,
                hashed_password,
            )

    return create_user_in_database


@pytest.fixture
async def create_posts_in_db(asyncpg_pool):
    async def create_posts_in_db(start_num: int = 200, count: int = 5):
        async with asyncpg_pool.acquire() as connection:
            for i in range(start_num, start_num + count):
                await connection.execute(
                    """INSERT INTO users VALUES ($1, $2, $3, $4)""",
                    i + 1,
                    f"test{i + 1}@example.com",
                    f"test{i + 1}",
                    f"testpass",
                )
                await connection.execute(
                    """INSERT INTO post (id, title, content, owner) VALUES ($1, $2, $3, $4)""",
                    i + 1,
                    f"Title {i + 1}",
                    f"Content {i + 1}",
                    i + 1,
                )

    return create_posts_in_db
