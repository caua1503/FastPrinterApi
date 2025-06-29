import pytest
import pytest_asyncio
import redis.asyncio as redis
from testcontainers.redis import RedisContainer


@pytest.fixture(scope="session")
def client_redis():
    with RedisContainer("redis:8.0") as redis_container:
        yield redis_container


@pytest_asyncio.fixture()
async def session_redis(client_redis):
    return redis.Redis(
        host=client_redis.get_container_host_ip(), port=client_redis.get_exposed_port(6379), decode_responses=True
    )
