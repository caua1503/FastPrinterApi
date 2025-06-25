from datetime import date

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from app.helpers.database_helper import get_session
from app.main import app
from app.models import table_registry
from app.models.department_model import Department
from app.models.history_model import (
    AlertHistory,
    MaintenanceHistory,
    PrinterTrashHistory,
    RefillHistory,
    StatusHistory,
)
from app.models.printer_model import Printer, Status
from app.models.supply_model import Supply, SupplyType
from app.models.user_model import User


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = "fake_password"
    user = User(
        login="testuser",
        name="testuser",
        password_hash="fake_password_hash",
        api_key="fake_api_key",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.password = password
    return user


@pytest_asyncio.fixture
async def supply(session: AsyncSession, supply_type: SupplyType):
    supply = Supply(
        name="Supply 1",
        description="Supply 1 description",
        brand="Brand 1",
        supply_type_id=supply_type.id,
    )
    session.add(supply)
    await session.commit()
    await session.refresh(supply)
    return supply


@pytest_asyncio.fixture
async def refill_history(session: AsyncSession, printer: Printer, supply: Supply) -> RefillHistory:
    new_history = RefillHistory(
        printer_id=printer.id,
        date=date.today(),
        event_type="Teste",
        supply_id=supply.id,
        description="description",
    )
    session.add(new_history)
    await session.commit()
    await session.refresh(new_history)
    return new_history


@pytest_asyncio.fixture
async def maintenance_history(session: AsyncSession, printer: Printer) -> MaintenanceHistory:
    new_history = MaintenanceHistory(
        printer_id=printer.id,
        date=date.today(),
        event_type="Teste",
        description="description",
    )
    session.add(new_history)
    await session.commit()
    await session.refresh(new_history)
    return new_history


@pytest_asyncio.fixture
async def supply_type(session: AsyncSession):
    supply_type = SupplyType(
        name="Supply Type 1",
    )
    session.add(supply_type)
    await session.commit()
    await session.refresh(supply_type)
    return supply_type


@pytest_asyncio.fixture
async def status(session: AsyncSession):
    status = Status(
        status="Status 1",
        description="Status 1 description",
    )
    session.add(status)
    await session.commit()
    await session.refresh(status)
    return status


@pytest_asyncio.fixture
async def department(session: AsyncSession):
    department = Department(
        name="TESTE",
        description="TESTE",
    )
    session.add(department)
    await session.commit()
    await session.refresh(department)
    return department


@pytest_asyncio.fixture
async def printer(session: AsyncSession, status: Status, supply: Supply, department: Department):
    printer = Printer(
        name="Printer 1",
        description="Printer 1 description",
        status_id=status.id,
        supply_id=supply.id,
        department_id=department.id,
        brand="Brand 1",
        model="Model 1",
        ip="192.168.1.1",
        forecast=date.today(),
        last_refill=date.today(),
        last_maintenance=date.today(),
        last_check=date.today(),
    )
    session.add(printer)
    await session.commit()
    await session.refresh(printer)
    return printer


@pytest_asyncio.fixture
async def printer2(session: AsyncSession, status: Status, supply: Supply, department: Department):
    printer = Printer(
        name="Printer 1",
        description="Printer 1 description",
        status_id=status.id,
        supply_id=supply.id,
        department_id=department.id,
        brand="Brand 1",
        model="Model 1",
        ip="192.168.1.2",
        forecast=date.today(),
        last_refill=date.today(),
        last_maintenance=date.today(),
        last_check=date.today(),
    )
    session.add(printer)
    await session.commit()
    await session.refresh(printer)
    return printer


@pytest_asyncio.fixture
async def supply2(session: AsyncSession, supply_type: SupplyType):
    supply = Supply(
        name="Supply 2",
        description="Supply 2 description",
        brand="Brand 2",
        supply_type_id=supply_type.id,
    )
    session.add(supply)
    await session.commit()
    await session.refresh(supply)
    return supply


@pytest_asyncio.fixture
async def printer_trash_history(session: AsyncSession, printer: Printer) -> PrinterTrashHistory:
    new_history = PrinterTrashHistory(
        printer_id=printer.id,
        date=date.today(),
        description="description",
    )
    session.add(new_history)
    await session.commit()
    await session.refresh(new_history)
    return new_history


@pytest_asyncio.fixture
async def alert_history(session: AsyncSession, printer: Printer) -> AlertHistory:
    new_history = AlertHistory(
        printer_id=printer.id,
        date=date.today(),
        alert_type="Test Alert",
        description="description",
    )
    session.add(new_history)
    await session.commit()
    await session.refresh(new_history)
    return new_history


@pytest_asyncio.fixture
async def status_history(session: AsyncSession, printer: Printer, status: Status) -> StatusHistory:
    new_history = StatusHistory(
        printer_id=printer.id,
        date=date.today(),
        status_id=status.id,
        description="description",
    )
    session.add(new_history)
    await session.commit()
    await session.refresh(new_history)
    return new_history


@pytest.fixture
def client(session: AsyncSession):
    def override_get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_get_session
        yield client

    # Limpa as dependências após o teste
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)
