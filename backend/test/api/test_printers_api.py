from http import HTTPStatus

import pytest

from app.models import Printer


@pytest.mark.asyncio
async def test_apirouter(client, token):
    response = client.get("/api/v1/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_printers(client, token):
    response = client.get("/api/v1/printer/", headers={"Authorization": f"Bearer {token}"})
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 0
    assert response_json["count"] == 0
    assert response_json["printers"] == []


@pytest.mark.asyncio
async def test_get_printers_with_printers(client, printer: Printer, token):
    response = client.get("/api/v1/printer/", headers={"Authorization": f"Bearer {token}"})
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert response_json["printers"][0]["id"] == printer.id
    assert response_json["printers"][0]["name"] == printer.name
    assert response_json["printers"][0]["brand"] == printer.brand
    assert response_json["printers"][0]["model"] == printer.model
    assert response_json["printers"][0]["ip"] == printer.ip
    assert response_json["printers"][0]["department_id"]["id"] == printer.department_id
    assert response_json["printers"][0]["supply_id"]["id"] == printer.supply_id
    assert response_json["printers"][0]["status_id"]["id"] == printer.status_id


@pytest.mark.asyncio
async def test_get_printer_by_id(client, printer: Printer, token):
    response = client.get(f"/api/v1/printer/{printer.id}", headers={"Authorization": f"Bearer {token}"})
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["name"] == printer.name
    assert response_json["brand"] == printer.brand
    assert response_json["model"] == printer.model
    assert response_json["ip"] == printer.ip
    assert response_json["department_id"]["id"] == printer.department_id
    assert response_json["supply_id"]["id"] == printer.supply_id
    assert response_json["status_id"]["id"] == printer.status_id
    assert response_json["description"] == printer.description
    assert response_json["forecast"] == printer.forecast.strftime("%Y-%m-%d") if printer.forecast else None
    assert response_json["last_refill"] == printer.last_refill.strftime("%Y-%m-%d") if printer.last_refill else None
    assert (
        response_json["last_maintenance"] == printer.last_maintenance.strftime("%Y-%m-%d")
        if printer.last_maintenance
        else None
    )
    assert response_json["last_check"] == printer.last_check.strftime("%Y-%m-%d") if printer.last_check else None


@pytest.mark.asyncio
async def test_create_printer(client, status, supply, department, token):
    data = {
        "name": "Printer 1",
        "brand": "Brand 1",
        "model": "Model 1",
        "ip": "192.168.1.1",
        "department_id": department.id,
        "supply_id": supply.id,
        "status_id": status.id,
        "description": "Description 1",
        "forecast": "2025-01-01",
        "last_refill": "2025-01-01",
        "last_maintenance": "2025-01-01",
        "last_check": "2025-01-01",
    }
    response = client.post("/api/v1/printer/", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["name"] == data["name"]
    assert response.json()["brand"] == data["brand"]
    assert response.json()["model"] == data["model"]
    assert response.json()["ip"] == data["ip"]
    assert response.json()["department_id"] == data["department_id"]
    assert response.json()["supply_id"] == data["supply_id"]
    assert response.json()["status_id"] == data["status_id"]


@pytest.mark.asyncio
async def test_create_printer_with_ip_already_exists(client, printer: Printer, token):
    data = {
        "name": "Printer 1",
        "brand": "Brand 1",
        "model": "Model 1",
        "ip": printer.ip,
        "department_id": 1,
        "supply_id": 1,
        "status_id": 1,
        "description": "Description 1",
        "forecast": "2025-01-01",
        "last_refill": "2025-01-01",
        "last_maintenance": "2025-01-01",
        "last_check": "2025-01-01",
    }
    response = client.post("/api/v1/printer/", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_update_printer(client, printer: Printer, status, supply, department, token):  # noqa: PLR0917, PLR0913
    data = {
        "name": "Printer 1",
        "brand": "Brand 1",
        "model": "Model 1",
        "ip": "192.168.1.1",
        "department_id": department.id,
        "supply_id": supply.id,
        "status_id": status.id,
        "description": "Description 1",
        "forecast": "2025-01-02",
        "last_refill": "2025-01-02",
        "last_maintenance": "2025-01-02",
        "last_check": "2025-01-02",
    }
    response = client.put(f"/api/v1/printer/{printer.id}", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert response.json()["forecast"] == "2025-01-02"
    assert response.json()["last_refill"] == "2025-01-02"
    assert response.json()["last_maintenance"] == "2025-01-02"
    assert response.json()["last_check"] == "2025-01-02"


@pytest.mark.asyncio
async def test_update_printer_with_ip_already_exists(client, printer: Printer, printer2: Printer, token):
    data = {
        "name": "Printer 1",
        "brand": "Brand 1",
        "model": "Model 1",
        "ip": printer.ip,
        "department_id": printer.department_id,
        "supply_id": printer.supply_id,
        "status_id": printer.status_id,
        "description": "Description 1",
        "forecast": "2025-01-01",
        "last_refill": "2025-01-01",
        "last_maintenance": "2025-01-01",
        "last_check": "2025-01-01",
    }
    response = client.put(f"/api/v1/printer/{printer2.id}", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_delete_printer(client, token):
    response = client.delete("/api/v1/printer/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_printer_with_printer_error(client, printer: Printer, token):
    response = client.delete(f"/api/v1/printer/{printer.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_get_printers_by_department_id(client, printer: Printer, token):
    response = client.get(
        f"/api/v1/printer/?department_id={printer.department_id}", headers={"Authorization": f"Bearer {token}"}
    )
    response_json = response.json()
    print(response_json)
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert response_json["printers"][0]["id"] == printer.id
    assert response_json["printers"][0]["name"] == printer.name
    assert response_json["printers"][0]["brand"] == printer.brand
    assert response_json["printers"][0]["model"] == printer.model
    assert response_json["printers"][0]["ip"] == printer.ip
    assert response_json["printers"][0]["department_id"]["id"] == printer.department_id
    assert response_json["printers"][0]["supply_id"]["id"] == printer.supply_id
    assert response_json["printers"][0]["status_id"]["id"] == printer.status_id


@pytest.mark.asyncio
async def test_get_printers_by_supply_id(client, printer: Printer, token):
    response = client.get(
        f"/api/v1/printer/?supply_id={printer.supply_id}", headers={"Authorization": f"Bearer {token}"}
    )
    response_json = response.json()
    print(response_json)
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert response_json["printers"][0]["id"] == printer.id
    assert response_json["printers"][0]["name"] == printer.name
    assert response_json["printers"][0]["brand"] == printer.brand
    assert response_json["printers"][0]["model"] == printer.model
    assert response_json["printers"][0]["ip"] == printer.ip
    assert response_json["printers"][0]["supply_id"]["id"] == printer.supply_id


@pytest.mark.asyncio
async def test_get_printers_by_status_id(client, printer: Printer, token):
    response = client.get(
        f"/api/v1/printer/?status_id={printer.status_id}", headers={"Authorization": f"Bearer {token}"}
    )
    response_json = response.json()
    print(response_json)
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert response_json["printers"][0]["id"] == printer.id
    assert response_json["printers"][0]["name"] == printer.name
    assert response_json["printers"][0]["brand"] == printer.brand
    assert response_json["printers"][0]["model"] == printer.model
    assert response_json["printers"][0]["ip"] == printer.ip
    assert response_json["printers"][0]["status_id"]["id"] == printer.status_id


@pytest.mark.asyncio
async def test_get_printers_by_multiple_filters(client, printer: Printer, token):
    url = (
        f"/api/v1/printer/?department_id={printer.department_id}"
        f"&supply_id={printer.supply_id}"
        f"&status_id={printer.status_id}"
    )
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert len(response_json["printers"]) == 1
    printer_json = response_json["printers"][0]
    assert printer_json["id"] == printer.id
    assert printer_json["department_id"]["id"] == printer.department_id
    assert printer_json["supply_id"]["id"] == printer.supply_id
    assert printer_json["status_id"]["id"] == printer.status_id
