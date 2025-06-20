from datetime import date

import pytest
from sqlalchemy import select

from app.models import (
    AlertHistory,
    Department,
    MaintenanceHistory,
    Printer,
    PrinterMaintenanceInfo,
    PrinterTrashHistory,
    RefillHistory,
    Status,
    StatusHistory,
    Supply,
    SupplyType,
)

porcentagem = 100


@pytest.mark.asyncio
async def test_create_printer_db(session, status, supply, department):
    printer = Printer(
        name="teste",
        model="teste",
        ip="192.168.1.1",
        brand="teste",
        department_id=department.id,
        status_id=status.id,
        supply_id=supply.id,
        description="teste",
        forecast=date.today(),
        last_refill=date.today(),
        last_maintenance=date.today(),
        last_check=date.today(),
    )

    session.add(printer)
    await session.commit()
    result = await session.scalar(select(Printer).where(Printer.ip == "192.168.1.1"))

    assert result.ip == "192.168.1.1"


@pytest.mark.asyncio
async def test_create_status_db(session):
    status = Status(status="teste", description="teste")
    session.add(status)
    await session.commit()
    result = await session.scalar(select(Status).where(Status.status == "teste"))
    assert result.status == "teste"
    assert result.description == "teste"


@pytest.mark.asyncio
async def test_create_supply_db(session, supply_type):
    supply = Supply(name="teste", supply_type_id=supply_type.id, brand="teste", description="teste")
    session.add(supply)
    await session.commit()
    result = await session.scalar(select(Supply).where(Supply.name == "teste"))
    assert result.name == "teste"
    assert result.supply_type_id == supply_type.id
    assert result.brand == "teste"
    assert result.description == "teste"


@pytest.mark.asyncio
async def test_create_supply_type_db(session):
    supply_type = SupplyType(name="teste")
    session.add(supply_type)
    await session.commit()
    result = await session.scalar(select(SupplyType).where(SupplyType.name == "teste"))
    assert result.name == "teste"


@pytest.mark.asyncio
async def test_create_department_db(session):
    department = Department(name="teste", description="teste")
    session.add(department)
    await session.commit()
    result = await session.scalar(select(Department).where(Department.name == "teste"))
    assert result.name == "teste"


@pytest.mark.asyncio
async def test_create_alert_history_db(session, printer):
    alert_history = AlertHistory(printer_id=printer.id, alert_type="teste", date=date.today(), description="teste")
    session.add(alert_history)
    await session.commit()
    result = await session.scalar(select(AlertHistory).where(AlertHistory.printer_id == printer.id))
    assert result.printer_id == printer.id
    assert result.alert_type == "teste"
    assert result.date == date.today()
    assert result.description == "teste"


@pytest.mark.asyncio
async def test_create_printer_maintenance_info_db(session, printer):
    printer_maintenance_info = PrinterMaintenanceInfo(
        printer_id=printer.id,
        last_update=date.today(),
        next_refill=date.today(),
        next_cleaning=date.today(),
        refill_percentage=porcentagem,
        cleaning_percentage=porcentagem,
    )
    session.add(printer_maintenance_info)
    await session.commit()
    result = await session.scalar(select(PrinterMaintenanceInfo).where(PrinterMaintenanceInfo.printer_id == printer.id))
    assert result.printer_id == printer.id
    assert result.last_update == date.today()
    assert result.next_refill == date.today()
    assert result.next_cleaning == date.today()
    assert result.refill_percentage == porcentagem
    assert result.cleaning_percentage == porcentagem


@pytest.mark.asyncio
async def test_create_refill_history_db(session, printer, supply):
    refill_history = RefillHistory(
        printer_id=printer.id, date=date.today(), event_type="teste", supply_id=supply.id, description="teste"
    )
    session.add(refill_history)
    await session.commit()
    result = await session.scalar(select(RefillHistory).where(RefillHistory.printer_id == printer.id))
    assert result.printer_id == printer.id
    assert result.date == date.today()
    assert result.event_type == "teste"
    assert result.supply_id == supply.id
    assert result.description == "teste"


@pytest.mark.asyncio
async def test_create_status_history_db(session, printer, status):
    status_history = StatusHistory(printer_id=printer.id, status_id=status.id, date=date.today(), description="teste")
    session.add(status_history)
    await session.commit()
    result = await session.scalar(select(StatusHistory).where(StatusHistory.printer_id == printer.id))
    assert result.printer_id == printer.id
    assert result.status_id == status.id
    assert result.date == date.today()


@pytest.mark.asyncio
async def test_create_maintenance_history_db(session, printer):
    maintenance_history = MaintenanceHistory(printer_id=printer.id, date=date.today(), event_type="teste", description="teste")
    session.add(maintenance_history)
    await session.commit()
    result = await session.scalar(select(MaintenanceHistory).where(MaintenanceHistory.printer_id == printer.id))
    assert result.printer_id == printer.id
    assert result.date == date.today()
    assert result.event_type == "teste"
    assert result.description == "teste"


@pytest.mark.asyncio
async def test_create_printer_trash_history_db(session, printer):
    printer_trash_history = PrinterTrashHistory(printer_id=printer.id, date=date.today(), description="teste")
    session.add(printer_trash_history)
    await session.commit()
    result = await session.scalar(select(PrinterTrashHistory).where(PrinterTrashHistory.printer_id == printer.id))
    assert result.printer_id == printer.id
    assert result.date == date.today()
    assert result.description == "teste"
