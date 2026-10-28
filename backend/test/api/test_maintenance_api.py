from datetime import date
from http import HTTPStatus

import pytest

from app.models.maintenance_model import PrinterMaintenanceInfo
from app.models.printer_model import Printer


@pytest.mark.asyncio
async def test_get_printer_maintenance_info_admin(client, printer: Printer, admin_token):
    response = client.get(
        f"/api/v1/core/current/info/printer/{printer.id}",
        params={"limit": 10, "offset": 0},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == printer.id
    assert "percentage" in data
    assert "next_recharge" in data
    assert "trash_cleaning_next_time" in data
    assert "trash_cleaning_percentage" in data


@pytest.mark.asyncio
async def test_get_printer_maintenance_info_service(client, printer: Printer, member_token):
    response = client.get(
        f"/api/v1/core/info/printer/{printer.id}",
        params={"limit": 10, "offset": 0},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == printer.id
    assert "printer_id" in data
    assert "department_id" in data
    assert "last_update" in data
    assert "refill_percentage" in data
    assert "next_refill" in data
    assert "next_cleaning" in data
    assert "cleaning_percentage" in data
    assert isinstance(data["refill_percentage"], float)
    assert isinstance(data["cleaning_percentage"], float)


@pytest.mark.asyncio
async def test_get_printer_maintenance_info_not_found(client, member_token):
    response = client.get(
        "/api/v1/core/info/printer/99999",
        params={"limit": 10, "offset": 0},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_all_printer_maintenance_info_empty(client, member_token):
    response = client.get(
        "/api/v1/core/info/printer",
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data == {"total": 0, "count": 0, "list": []}


@pytest.mark.asyncio
async def test_get_all_printer_maintenance_info_two_printers(client, session, printer: Printer, member_token):
    printer2 = Printer(
        name="Printer 2",
        description="Printer 2 description",
        status_id=printer.status_id,
        supply_id=printer.supply_id,
        department_id=printer.department_id,
        brand="Brand 2",
        model="Model 2",
        ip="192.168.1.20",
        forecast=date.today(),
        last_refill=date.today(),
        last_maintenance=date.today(),
        last_check=date.today(),
    )
    session.add(printer2)
    await session.commit()
    await session.refresh(printer2)

    info1 = PrinterMaintenanceInfo(
        printer_id=printer.id,
        last_update=date.today(),
        next_refill=date.today(),
        next_cleaning=date.today(),
        refill_percentage=80.0,
        cleaning_percentage=20.0,
    )
    info2 = PrinterMaintenanceInfo(
        printer_id=printer2.id,
        last_update=date.today(),
        next_refill=date.today(),
        next_cleaning=date.today(),
        refill_percentage=90.0,
        cleaning_percentage=10.0,
    )
    session.add_all([info1, info2])
    await session.commit()

    response = client.get(
        "/api/v1/core/info/printer",
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    expected_total = 2
    assert data["total"] == expected_total
    assert data["count"] == expected_total
    assert len(data["list"]) == expected_total

    item1 = data["list"][0]
    assert item1["department_id"] == {"id": printer.department.id, "name": printer.department.name}
    assert "printer_id" in item1
    assert "last_update" in item1
    assert "next_refill" in item1
    assert "next_cleaning" in item1
    assert "refill_percentage" in item1
    assert "cleaning_percentage" in item1


@pytest.mark.asyncio
async def test_get_all_printer_maintenance_info_pagination(client, session, printer: Printer, member_token):
    printer2 = Printer(
        name="Printer 2",
        description="Printer 2 description",
        status_id=printer.status_id,
        supply_id=printer.supply_id,
        department_id=printer.department_id,
        brand="Brand 2",
        model="Model 2",
        ip="192.168.1.20",
        forecast=date.today(),
        last_refill=date.today(),
        last_maintenance=date.today(),
        last_check=date.today(),
    )
    session.add(printer2)
    await session.commit()
    await session.refresh(printer2)

    info1 = PrinterMaintenanceInfo(
        printer_id=printer.id,
        last_update=date.today(),
        next_refill=date.today(),
        next_cleaning=date.today(),
        refill_percentage=80.0,
        cleaning_percentage=20.0,
    )
    info2 = PrinterMaintenanceInfo(
        printer_id=printer2.id,
        last_update=date.today(),
        next_refill=date.today(),
        next_cleaning=date.today(),
        refill_percentage=90.0,
        cleaning_percentage=10.0,
    )
    session.add_all([info1, info2])
    await session.commit()

    response = client.get(
        "/api/v1/core/info/printer",
        params={"limit": 1, "offset": 1},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    expected_total = 2
    expected_count = 1
    assert data["total"] == expected_total
    assert data["count"] == expected_count
    assert len(data["list"]) == expected_count
