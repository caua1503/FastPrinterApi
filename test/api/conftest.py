from datetime import date

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
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
from app.schemas.user_schema import UsersRoleSchema


@pytest_asyncio.fixture
async def token(client: TestClient, user: User):
    response = client.post("/api/v1/auth/token", data={"username": user.login, "password": user.password})  # type: ignore
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def admin_token(client: TestClient, admin_user: User):
    response = client.post("/api/v1/auth/token", data={"username": admin_user.login, "password": admin_user.password})  # type: ignore
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = "fake_password"
    user = User(
        login="testuser",
        name="testuser",
        password_hash=get_password_hash(password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.password = password  # type: ignore
    return user


@pytest_asyncio.fixture
async def admin_user(session: AsyncSession):
    password = "fake_password"
    user = User(
        login="admin",
        name="admin",
        role=UsersRoleSchema.admin,
        password_hash=get_password_hash(password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.password = password  # type: ignore
    return user


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
