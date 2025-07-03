import pytest
import pytest_asyncio
import redis.asyncio as redis
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from app.helpers.database_helper import get_redis_client, get_session
from app.main import app
from app.models import table_registry

pytest_plugins = ["db_fixture"]


@pytest.fixture
def client(session: AsyncSession, session_redis: redis.Redis):
    def override_get_session():
        return session

    def override_get_redis_client():
        return session_redis

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_get_session
        app.dependency_overrides[get_redis_client] = override_get_redis_client
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:17", driver="psycopg") as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest.fixture(scope="session")
def client_redis():
    with RedisContainer("redis:8.0") as redis_container:
        yield redis_container


@pytest_asyncio.fixture()
async def session_redis(client_redis):
    return redis.Redis(
        host=client_redis.get_container_host_ip(), port=client_redis.get_exposed_port(6379), decode_responses=True
    )


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)
