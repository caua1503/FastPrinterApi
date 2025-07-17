from http import HTTPStatus

import pytest

from app.models.printer_model import Printer, Status


@pytest.mark.asyncio
async def test_create_status(client, token):
    response = client.post(
        "/api/v1/status/",
        json={"status": "Test Status", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["status"] == "Test Status"
    assert data["description"] == "Test Description"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_status(client, status: Status, token):
    response = client.get("/api/v1/status/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "status" in data
    assert len(data["status"]) == 1
    assert data["status"][0]["status"] == status.status
    assert data["status"][0]["description"] == status.description


@pytest.mark.asyncio
async def test_get_status_not_found(client, token):
    response = client.get("/api/v1/status/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_status_by_id(client, status: Status, token):
    response = client.get(f"/api/v1/status/{status.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["status"] == status.status
    assert data["description"] == status.description


@pytest.mark.asyncio
async def test_get_status_by_id_not_found(client, token):
    response = client.get("/api/v1/status/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_update_status(client, status: Status, token):
    response = client.put(
        f"/api/v1/status/{status.id}",
        json={"status": "Updated Status", "description": "Updated Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["status"] == "Updated Status"
    assert data["description"] == "Updated Description"


@pytest.mark.asyncio
async def test_update_status_not_found(client, token):
    response = client.put(
        "/api/v1/status/999",
        json={"status": "Updated Status", "description": "Updated Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_status(client, status: Status, printer: Printer, token):
    response = client.delete(f"/api/v1/printer/{printer.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NO_CONTENT
    response = client.delete(f"/api/v1/status/{status.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_status_not_found(client, token):
    response = client.delete("/api/v1/status/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_status_with_printer_associated(client, printer: Printer, token):
    response = client.delete(f"/api/v1/status/{printer.status_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Status has printers"
