import asyncio
import json
from http import HTTPStatus
from typing import Any, List, Optional, Type, Union

import redis.asyncio as redis
from fastapi import HTTPException

from app.core.logs import create_redis_log
from app.helpers.database_helper import get_redis_client
from app.helpers.utils_helper import ModelType, deserialize_data, serialize_data

"""
    (redis_client: Optional[redis.Redis] = None)

    This and to take advantage od a single connection with the bank
    for multiple operations, if not past it gets a new connection

"""


async def verify_redis_value(key: str, redis_client: Optional[redis.Redis] = None) -> bool:
    if redis_client is None:
        redis_client = await get_redis_client()
    exists = await redis_client.exists(key)
    return True if exists == 1 else False


async def redis_set_value(key: str, value: Any, redis_client: Optional[redis.Redis] = None, **kwargs):
    try:
        if redis_client is None:
            redis_client = await get_redis_client()

        await redis_client.set(key, json.dumps(value), **kwargs)
        return True
    except Exception as erro:
        asyncio.create_task(create_redis_log(erro))
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error connecting to Redis")


async def redis_get_value(key: str, redis_client: Optional[redis.Redis] = None):
    try:
        if redis_client is None:
            redis_client = await get_redis_client()

        result = await redis_client.get(key)

        if result:
            return json.loads(result)

        return False
    except Exception as erro:
        asyncio.create_task(create_redis_log(erro))
        raise erro


async def redis_set_value_pydantic(
    key: str,
    value: Union[ModelType, List[ModelType]],
    redis_client: Optional[redis.Redis] = None,
    invalid_json: bool = False,
    **kwargs,
):
    """
    a function to save Pydantic models in Redis
    Args:
        value: The value can be a model or list of models,
        this is handled internally by the function automatically by the function
        redis_client (Optional[redis.Redis]): Redis client, which can pass or get automatically
        **kwargs : accept all redis.set() functions
    return:
        True (bool): Opicional, indicates that it was successfully saved

    """
    if invalid_json:
        ...
    return await redis_set_value(key, serialize_data(value), redis_client, **kwargs)


async def redis_get_value_pydantic(
    key: str,
    model: Type[ModelType],
    is_list: bool = False,
    redis_client: Optional[redis.Redis] = None,
):
    result = await redis_get_value(key, redis_client)
    return deserialize_data(str(result), model, is_list)
