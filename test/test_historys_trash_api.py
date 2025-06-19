from datetime import date
from http import HTTPStatus

from app.models.history_model import PrinterTrashHistory
from app.models.printer_model import Printer


def test_get_history_trash_empty(client):
    response = client.get("/api/v1/history/trash")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"historys": []}


def test_get_history_trash(client, printer_trash_history: PrinterTrashHistory):
    response = client.get("/api/v1/history/trash")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["historys"][0]["id"] == printer_trash_history.id
    assert response_json["historys"][0]["printer_id"] == printer_trash_history.printer_id
    assert response_json["historys"][0]["date"] == printer_trash_history.date.strftime("%Y-%m-%d")
    assert response_json["historys"][0]["description"] == printer_trash_history.description


def test_create_history_trash(client, printer: Printer):
    response = client.post(
        "/api/v1/history/trash",
        json={
            "printer_id": printer.id,
            "date": date.today().strftime("%Y-%m-%d"),
            "description": "Test description",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json["printer_id"] == printer.id
    assert response_json["description"] == "Test description"
    assert "id" in response_json


def test_update_history_trash(client, printer_trash_history: PrinterTrashHistory):
    new_description = "Updated description"
    response = client.put(
        f"/api/v1/history/trash/{printer_trash_history.id}",
        json={
            "printer_id": printer_trash_history.printer_id,
            "date": date.today().strftime("%Y-%m-%d"),
            "description": new_description,
        },
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == printer_trash_history.id
    assert response_json["description"] == new_description


def test_get_history_trash_by_printer_id(client, printer_trash_history: PrinterTrashHistory, printer: Printer):
    response = client.get(f"/api/v1/history/trash/printer/{printer.id}")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(response_json["historys"]) > 0
    assert response_json["historys"][0]["printer_id"] == printer.id
    assert response_json["historys"][0]["id"] == printer_trash_history.id


def test_delete_history_trash(client, printer_trash_history: PrinterTrashHistory):
    response = client.delete(f"/api/v1/history/trash/{printer_trash_history.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_history_trash_not_found(client):
    response = client.delete("/api/v1/history/trash/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND
