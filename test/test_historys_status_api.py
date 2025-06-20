from datetime import date
from http import HTTPStatus

from app.models.history_model import StatusHistory


def test_get_history_status_empty(client):
    response = client.get("/api/v1/history/status")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"historys": []}


def test_get_history_status(client, status_history: StatusHistory):
    response = client.get("/api/v1/history/status")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(response_json["historys"]) > 0
    assert response_json["historys"][0]["id"] == status_history.id
    assert response_json["historys"][0]["printer_id"] == status_history.printer_id
    assert response_json["historys"][0]["date"] == status_history.date.strftime("%Y-%m-%d")
    assert response_json["historys"][0]["status_id"] == status_history.status_id
    assert response_json["historys"][0]["description"] == status_history.description


def test_get_history_status_by_id(client, status_history: StatusHistory):
    response = client.get(f"/api/v1/history/status/{status_history.id}")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["id"] == status_history.id
    assert response_json["printer_id"] == status_history.printer_id
    assert response_json["date"] == status_history.date.strftime("%Y-%m-%d")
    assert response_json["status_id"] == status_history.status_id
    assert response_json["description"] == status_history.description


def test_update_history_status(client, status_history: StatusHistory):
    new_description = "Updated description"
    response = client.put(
        f"/api/v1/history/status/{status_history.id}",
        json={
            "printer_id": status_history.printer_id,
            "status_id": status_history.status_id,
            "date": date.today().strftime("%Y-%m-%d"),
            "description": new_description,
        },
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == status_history.id
    assert response_json["description"] == new_description
    assert response_json["status_id"] == status_history.status_id


def test_delete_history_status(client, status_history: StatusHistory):
    response = client.delete(f"/api/v1/history/status/{status_history.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_history_status_not_found(client):
    response = client.delete("/api/v1/history/status/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND
