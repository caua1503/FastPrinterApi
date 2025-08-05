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


async def get_redis_client() -> redis.Redis:
    try:
        return redis.Redis(connection_pool=pool, decode_responses=True)
    except Exception as erro:
        from app.core.celery.tasks.logs import create_redis_log  # noqa: PLC0415

        asyncio.create_task(create_redis_log(erro, LogLevelSchema.CRITICAL))
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error connecting to Redis")
