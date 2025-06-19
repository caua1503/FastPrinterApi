from datetime import date
from http import HTTPStatus

from app.models.history_model import MaintenanceHistory
from app.models.printer_model import Printer


def test_get_history_maintenance_empty(client):
    response = client.get("/api/v1/history/maintenance")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"historys": []}


def test_get_history_maintenance(client, maintenance_history: MaintenanceHistory):
    response = client.get("/api/v1/history/maintenance")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["historys"][0]["id"] == maintenance_history.id
    assert response_json["historys"][0]["printer_id"] == maintenance_history.printer_id
    assert response_json["historys"][0]["date"] == maintenance_history.date.strftime("%Y-%m-%d")
    assert response_json["historys"][0]["event_type"] == maintenance_history.event_type
    assert response_json["historys"][0]["description"] == maintenance_history.description


def test_get_history_maintenance_by_id(client, maintenance_history: MaintenanceHistory):
    response = client.get(f"/api/v1/history/maintenance/{maintenance_history.id}")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["id"] == maintenance_history.id
    assert response_json["printer_id"] == maintenance_history.printer_id
    assert response_json["date"] == maintenance_history.date.strftime("%Y-%m-%d")
    assert response_json["event_type"] == maintenance_history.event_type
    assert response_json["description"] == maintenance_history.description


def test_create_history_maintenance(client, printer: Printer):
    response = client.post(
        "/api/v1/history/maintenance",
        json={
            "printer_id": printer.id,
            "date": date.today().strftime("%Y-%m-%d"),
            "event_type": "Test Maintenance",
            "description": "Test description",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json["printer_id"] == printer.id
    assert response_json["description"] == "Test description"
    assert "id" in response_json


def test_update_history_maintenance(client, maintenance_history: MaintenanceHistory):
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
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == maintenance_history.id
    assert response_json["description"] == new_description
    assert response_json["event_type"] == new_event_type


def test_get_history_maintenance_by_printer_id(client, maintenance_history: MaintenanceHistory, printer: Printer):
    response = client.get(f"/api/v1/history/maintenance/printer/{printer.id}")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(response_json["historys"]) > 0
    assert response_json["historys"][0]["printer_id"] == printer.id
    assert response_json["historys"][0]["id"] == maintenance_history.id


def test_delete_history_maintenance(client, maintenance_history: MaintenanceHistory):
    response = client.delete(f"/api/v1/history/maintenance/{maintenance_history.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_history_maintenance_not_found(client):
    response = client.delete("/api/v1/history/maintenance/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND
