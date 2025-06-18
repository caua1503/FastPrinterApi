import os
import sys

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
app_path = os.path.join(project_root, "app")
sys.path.insert(1, app_path)

from app.helpers.database_helper import get_session
from app.main import app
from app.models import table_registry



@pytest.fixture
def client(session):
    def override_get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_get_session
        yield client

    # Limpa as dependências após o teste
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


