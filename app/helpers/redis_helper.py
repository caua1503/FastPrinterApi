import asyncio
import json
from typing import Any, Optional, Union

import redis.asyncio as redis

from app.config import Config
from app.core.logs import create_redis_log

config = Config()

pool = redis.ConnectionPool(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
)


"""
    (redis_client: Optional[redis.Redis] = None)

    This and to take advantage od a single connection with the bank
    for multiple operations, if not past it gets a new connection

"""


async def get_redis_client() -> redis.Redis:
    try:
        return redis.Redis(connection_pool=pool)
    except Exception as erro:
        raise erro


async def verify_redis_value(key: str, redis_client: Optional[redis.Redis] = None) -> bool:
    if redis_client is None:
        redis_client = await get_redis_client()
    exists = await redis_client.exists(key)
    return True if exists == 1 else False


async def redis_set_value(key: str, value: Any, redis_client: Optional[redis.Redis] = None) -> bool:
    if redis_client is None:
        redis_client = await get_redis_client()
    try:
        result = await redis_client.set(key, json.dumps(value))
    except Exception as erro:
        asyncio.create_task(create_redis_log(erro))
        return False

    return result


async def redis_get_value(key: str, redis_client: Optional[redis.Redis] = None) -> Union[Any, bool]:
    if redis_client is None:
        redis_client = await get_redis_client()

    result = await redis_client.get(key)

    if result:
        return json.loads(result.decode("utf-8"))

    return False
