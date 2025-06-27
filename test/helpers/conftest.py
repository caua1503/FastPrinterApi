import pytest
import pytest_asyncio
import redis.asyncio as redis
from testcontainers.redis import RedisContainer


@pytest.fixture(scope="session")
def client_redis():
    with RedisContainer("redis:8.0") as redis:
        _redis = redis.get_client()
        yield _redis


@pytest_asyncio.fixture()
async def session_redis(client_redis):
    return redis.Redis(decode_responses=True)
