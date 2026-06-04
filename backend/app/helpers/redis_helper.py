import json
from http import HTTPStatus
from typing import Any, List, Optional, Type, Union

import redis.asyncio as redis
from fastapi import HTTPException

from app.helpers.database_helper import get_redis_client
from app.helpers.utils_helper import (
    ModelType,
    deserialize_data,
    deserialize_from_json,
    serialize_data,
    serialize_from_json,
)

"""
    (redis_client: Optional[redis.Redis] = None)

    This and to take advantage od a single connection with the bank
    for multiple operations, if not past it gets a new connection

"""


async def redis_verify_value(key: str, redis_client: Optional[redis.Redis] = None) -> bool:
    """
    Verify if a value exists in Redis
    Args:
        key: Redis key to verify
        redis_client: Optional Redis client
    return:
        True (bool): If the value exists or False if not
    """

    try:
        if redis_client is None:
            redis_client = await get_redis_client()
        exists = await redis_client.exists(key)
        return True if exists == 1 else False
    except Exception as error:
        raise error


async def redis_set_value(key: str, value: Any, redis_client: Optional[redis.Redis] = None, **kwargs):
    """
    Args:
        key: Redis key to save
        value: The value to save
        redis_client: Optional Redis client
        **kwargs : accept all redis.set() functions
    return:
        True (bool): Opicional, indicates that it was successfully saved
    """
    try:
        if redis_client is None:
            redis_client = await get_redis_client()

        await redis_client.set(key, json.dumps(value), **kwargs)
        return True
    except Exception:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error connecting to Redis")


async def redis_delete_value(key: str, redis_client: Optional[redis.Redis] = None):
    try:
        if redis_client is None:
            redis_client = await get_redis_client()

        await redis_client.delete(key)

        return True
    except Exception:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error connecting to Redis")


async def redis_get_value(key: str, redis_client: Optional[redis.Redis] = None):
    """
    Get a value from Redis
    Args:
        key: Redis key to get
        redis_client: Optional Redis client
    return:
        The value from Redis or None if not found
    """
    try:
        if redis_client is None:
            redis_client = await get_redis_client()

        result = await redis_client.get(key)

        if result:
            return json.loads(result)

        return None
    except Exception as erro:
        raise erro


async def redis_set_value_pydantic(
    key: str,
    value: Union[ModelType, List[ModelType]],
    redis_client: Optional[redis.Redis] = None,
    valid_json: bool = True,
    **kwargs,
):
    """
    a function to save Pydantic models in Redis
    Args:
        value: The value can be a model or list of models,
        this is handled internally by the function automatically by the function
        redis_client (Optional[redis.Redis]): Redis client, which can pass or get automatically
        valid_json (bool): If True, uses standard JSON serialization. If False, handles special types like dates
        **kwargs : accept all redis.set() functions
    return:
        True (bool): Opicional, indicates that it was successfully saved
    """
    if valid_json:
        serialized_value = serialize_data(value)
    else:
        serialized_value = json.dumps(serialize_from_json(value), default=str)

    return await redis_set_value(key, serialized_value, redis_client, **kwargs)


async def redis_get_value_pydantic(
    key: str,
    model: Type[ModelType],
    is_list: bool = False,
    redis_client: Optional[redis.Redis] = None,
    valid_json: bool = True,
):
    """
    a function to retrieve Pydantic models from Redis
    Args:
        key: Redis key to retrieve
        model: Pydantic model class to deserialize into
        is_list: Whether to expect a list of models
        redis_client: Optional Redis client
        valid_json: If True, uses standard JSON deserialization. If False, handles special types like dates
    return:
        Union[ModelType, List[ModelType]]: The deserialized model(s) or None if not found
    """
    result = await redis_get_value(key, redis_client)

    if not result:
        return None

    if valid_json:
        return deserialize_data(result, model, is_list)
    else:
        if is_list:
            data_list = json.loads(result)
            return [deserialize_from_json(item, model) for item in data_list]
        return deserialize_from_json(json.loads(result), model)
