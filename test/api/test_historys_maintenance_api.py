from datetime import date
from http import HTTPStatus

import pytest

from app.models.history_model import MaintenanceHistory
from app.models.printer_model import Printer


@pytest.mark.asyncio
async def test_get_history_maintenance_empty(client, token):
    response = client.get("/api/v1/history/maintenance", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"historys": [], "total": 0, "count": 0}


@pytest.mark.asyncio
async def test_get_history_maintenance(client, maintenance_history: MaintenanceHistory, token):
    response = client.get("/api/v1/history/maintenance", headers={"Authorization": f"Bearer {token}"})
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert response_json["historys"][0]["id"] == maintenance_history.id
    assert response_json["historys"][0]["printer_id"] == maintenance_history.printer_id
    assert response_json["historys"][0]["date"] == maintenance_history.date.strftime("%Y-%m-%d")
    assert response_json["historys"][0]["event_type"] == maintenance_history.event_type
    assert response_json["historys"][0]["description"] == maintenance_history.description


@pytest.mark.asyncio
async def test_get_history_maintenance_by_id(client, maintenance_history: MaintenanceHistory, token):
    response = client.get(
        f"/api/v1/history/maintenance/{maintenance_history.id}", headers={"Authorization": f"Bearer {token}"}
    )
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["id"] == maintenance_history.id
    assert response_json["printer_id"] == maintenance_history.printer_id
    assert response_json["date"] == maintenance_history.date.strftime("%Y-%m-%d")
    assert response_json["event_type"] == maintenance_history.event_type
    assert response_json["description"] == maintenance_history.description


@pytest.mark.asyncio
async def test_create_history_maintenance(client, printer: Printer, token):
    response = client.post(
        "/api/v1/history/maintenance",
        json={
            "printer_id": printer.id,
            "date": date.today().strftime("%Y-%m-%d"),
            "event_type": "Test Maintenance",
            "description": "Test description",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json["printer_id"] == printer.id
    assert response_json["description"] == "Test description"
    assert "id" in response_json


@pytest.mark.asyncio
async def test_update_history_maintenance(client, maintenance_history: MaintenanceHistory, token):
    new_description = "Updated description"
    new_event_type = "Updated event type"
    response = client.put(
        f"/api/v1/history/maintenance/{maintenance_history.id}",
        json={
            "printer_id": maintenance_history.printer_id,
            "date": date.today().strftime("%Y-%m-%d"),
            "event_type": new_event_type,
            "description": new_description,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == maintenance_history.id
    assert response_json["description"] == new_description
    assert response_json["event_type"] == new_event_type


@pytest.mark.asyncio
async def test_get_history_maintenance_by_printer_id(
    client, maintenance_history: MaintenanceHistory, printer: Printer, token
):
    response = client.get(
        f"/api/v1/history/maintenance?printer_id={printer.id}", headers={"Authorization": f"Bearer {token}"}
    )
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert len(response_json["historys"]) > 0
    assert response_json["historys"][0]["printer_id"] == printer.id
    assert response_json["historys"][0]["id"] == maintenance_history.id


@pytest.mark.asyncio
async def test_delete_history_maintenance(client, maintenance_history: MaintenanceHistory, token):
    response = client.delete(
        f"/api/v1/history/maintenance/{maintenance_history.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_history_maintenance_not_found(client, token):
    response = client.delete("/api/v1/history/maintenance/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND
