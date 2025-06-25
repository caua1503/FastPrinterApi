import asyncio
from http import HTTPStatus

import redis.asyncio as redis
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config import Config
from app.core.logs import create_redis_log
from app.schemas.logs_schema import LogLevelSchema

config = Config() # pyright: ignore

engine = create_async_engine(config.DATABASE_URL)

engine_logs = create_async_engine(config.DATABASE_LOGS_URL)

pool = redis.ConnectionPool(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session


async def get_session_logs():
    async with AsyncSession(engine_logs) as session_logs:
        yield session_logs

async def get_redis_client() -> redis.Redis:
    try:
        return redis.Redis(connection_pool=pool, decode_responses=True)
    except Exception as erro:
        asyncio.create_task(create_redis_log(erro, LogLevelSchema.CRITICAL))
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error connecting to Redis")