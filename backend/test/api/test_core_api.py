from http import HTTPStatus

import pytest

from app.models.printer_model import Printer


@pytest.mark.asyncio
async def test_get_all_printers_maintenance_info(client, printer: Printer, token):
    response = client.get(
        "/api/v1/core/current/info/printer/all",
        params={"limit": 10, "offset": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_printer_maintenance_info(client, printer: Printer, token):
    response = client.get(
        f"/api/v1/core/current/info/printer/{printer.id}",
        params={"limit": 10, "offset": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_all_printers_maintenance_info_admin(client, printer: Printer, admin_token):
    response = client.get(
        "/api/v1/core/current/info/printer/all",
        params={"limit": 10, "offset": 0},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)
    assert any(p["id"] == printer.id for p in data)


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
async def test_get_printer_maintenance_info_service(client, printer: Printer, token):
    response = client.get(
        f"/api/v1/core/info/printer/{printer.id}",
        params={"limit": 10, "offset": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == printer.id
    assert "percentage" in data
    assert "next_recharge" in data
    assert "trash_cleaning_next_time" in data
    assert "trash_cleaning_percentage" in data


@pytest.mark.asyncio
async def test_get_printer_maintenance_info_not_found(client, token):
    response = client.get(
        "/api/v1/core/info/printer/99999",
        params={"limit": 10, "offset": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
