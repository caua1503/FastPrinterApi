import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
app_path = os.path.join(project_root, "app")
sys.path.insert(1, app_path)

from helpers.database_helper import get_session
from app.main import app
from app.models.model_db import table_registry


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def override_get_session():
        yield session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_get_session
        yield client

    # Limpa as dependências após o teste
    app.dependency_overrides.clear()
