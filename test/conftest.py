import os
import sys
import pytest
from fastapi.testclient import TestClient 
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
app_path = os.path.join(project_root, 'app')
sys.path.insert(1, app_path)

from app.main import app
from app.models.model_db import Impressora, table_registry

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture()
def session():
    engine = create_engine("sqlite:///:memory:")
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)