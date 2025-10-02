import asyncio
from datetime import datetime
from http import HTTPStatus

import redis.asyncio as redis
from fastapi import HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config import get_config
from app.schemas.logs_schema import LogLevelSchema, ServiceSchema, SystemLogSchema

config = get_config()  # pyright: ignore

engine = create_async_engine(config.DATABASE_URL)

engine_logs = create_async_engine(config.DATABASE_LOGS_URL)

pool = redis.ConnectionPool(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    max_connections=10,
    retry_on_timeout=True,
    socket_keepalive=True,
    socket_keepalive_options={},
)


async def get_session():
    try:
        async with AsyncSession(engine) as session:
            yield session
    except OperationalError as e:
        log = SystemLogSchema(
            message=f"Error connecting to database: {e}",
            description="Database connection error",
            level=LogLevelSchema.CRITICAL,
            service=ServiceSchema.POSTGRES,
            timestamp=datetime.now(),
        )
        from app.core.celery.tasks.logs import task_create_log  # noqa: PLC0415

        task_create_log.delay("system", **log.model_dump())
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error connecting to database")


async def get_session_logs():
    try:
        async with AsyncSession(engine_logs) as session_logs:
            yield session_logs
    except OperationalError:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error connecting to database")


# Singleton global para reutilizar a mesma instância do Redis
_redis_client = None


async def get_redis_client() -> redis.Redis:
    try:
        global _redis_client  # noqa: PLW0603
        if _redis_client is None:
            _redis_client = redis.Redis(connection_pool=pool, decode_responses=True)
        return _redis_client
    except Exception as erro:
        from app.core.celery.tasks.logs import create_redis_log  # noqa: PLC0415

        asyncio.create_task(create_redis_log(erro, LogLevelSchema.CRITICAL))
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error connecting to Redis")
