from datetime import date

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department_model import Department
from app.models.printer_model import Printer, Status
from app.models.supply_model import Supply, SupplyType


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
