import json
from typing import Any, Union

import redis.asyncio as redis
from config import Config

pool = redis.ConnectionPool(host=Config().REDIS_HOST, port=Config().REDIS_PORT, db=0)


async def get_redis_client() -> redis.Redis:
    return redis.Redis(connection_pool=pool)


async def set_value(key: str, value: Any) -> bool:
    client = await get_redis_client()
    result = await client.set(key, json.dumps(value))
    if result:
        return True
    return False


async def get_value(key: str) -> Union[Any, bool]:
    client = await get_redis_client()
    result = await client.get(key)
    if result:
        return json.loads(result.decode("utf-8"))
    return False
