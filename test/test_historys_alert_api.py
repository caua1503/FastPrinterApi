from datetime import date
from http import HTTPStatus

from app.models.history_model import AlertHistory
from app.models.printer_model import Printer


def test_get_history_alert_empty(client):
    response = client.get("/api/v1/history/alert")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"historys": []}


def test_get_history_alert(client, alert_history: AlertHistory):
    response = client.get("/api/v1/history/alert")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["historys"][0]["id"] == alert_history.id
    assert response_json["historys"][0]["printer_id"] == alert_history.printer_id
    assert response_json["historys"][0]["date"] == alert_history.date.strftime("%Y-%m-%d")
    assert response_json["historys"][0]["alert_type"] == alert_history.alert_type
    assert response_json["historys"][0]["description"] == alert_history.description


def test_update_history_alert(client, alert_history: AlertHistory):
    new_description = "Updated description"
    new_alert_type = "Updated alert type"
    response = client.put(
        f"/api/v1/history/alert/{alert_history.id}",
        json={
            "printer_id": alert_history.printer_id,
            "date": date.today().strftime("%Y-%m-%d"),
            "alert_type": new_alert_type,
            "description": new_description,
        },
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == alert_history.id
    assert response_json["description"] == new_description
    assert response_json["alert_type"] == new_alert_type


def test_get_history_alert_by_printer_id(client, alert_history: AlertHistory, printer: Printer):
    response = client.get(f"/api/v1/history/alert?printer_id={printer.id}")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(response_json["historys"]) > 0
    assert response_json["historys"][0]["printer_id"] == printer.id
    assert response_json["historys"][0]["id"] == alert_history.id


def test_delete_history_alert(client, alert_history: AlertHistory):
    response = client.delete(f"/api/v1/history/alert/{alert_history.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_history_alert_not_found(client):
    response = client.delete("/api/v1/history/alert/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND
