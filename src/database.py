from redis import asyncio as aioredis
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker

from src.config import setting

DATABASE_URL = f"postgresql+asyncpg://{setting.DB_USER}:{setting.DB_PASS}@{setting.DB_HOST}:{setting.DB_PORT}/{setting.DB_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_redis_connection() -> Redis:
    redis = await aioredis.from_url(f"redis://localhost:{setting.REDIS_PORT}")
    return redis
