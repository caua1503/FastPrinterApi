from datetime import date
from http import HTTPStatus

from app.models.history_model import RefillHistory
from app.models.printer_model import Printer
from app.models.supply_model import Supply


def test_get_history_recharge_empty(client):
    response = client.get("/api/v1/history/recharge")
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"historys": []}


def test_get_history_recharge(client, refill_history: RefillHistory):
    response = client.get("/api/v1/history/recharge")
    print(response.json())
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["historys"][0]["id"] == refill_history.id
    assert response_json["historys"][0]["printer_id"] == refill_history.printer_id
    assert response_json["historys"][0]["date"] == refill_history.date.strftime("%Y-%m-%d")
    assert response_json["historys"][0]["event_type"] == refill_history.event_type
    assert response_json["historys"][0]["supply_id"] == refill_history.supply_id
    assert response_json["historys"][0]["description"] == refill_history.description


def test_get_history_recharge_by_id(client, refill_history: RefillHistory):
    response = client.get(f"/api/v1/history/recharge/{refill_history.id}")
    print(response.json())
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["id"] == refill_history.id
    assert response_json["printer_id"] == refill_history.printer_id
    assert response_json["date"] == refill_history.date.strftime("%Y-%m-%d")
    assert response_json["event_type"] == refill_history.event_type
    assert response_json["supply_id"] == refill_history.supply_id
    assert response_json["description"] == refill_history.description


def test_create_history_recharge(client, printer: Printer, supply: Supply):
    response = client.post(
        "/api/v1/history/recharge",
        json={
            "printer_id": printer.id,
            "date": date.today().strftime("%Y-%m-%d"),
            "event_type": "Test Recharge",
            "supply_id": supply.id,
            "description": "Test description",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json["printer_id"] == printer.id
    assert response_json["supply_id"] == supply.id
    assert response_json["description"] == "Test description"
    assert "id" in response_json


def test_update_history_recharge(client, refill_history: RefillHistory, supply2: Supply):
    new_description = "Updated description"
    new_event_type = "Updated event type"
    response = client.put(
        f"/api/v1/history/recharge/{refill_history.id}",
        json={
            "printer_id": refill_history.printer_id,
            "date": date.today().strftime("%Y-%m-%d"),
            "event_type": new_event_type,
            "supply_id": supply2.id,
            "description": new_description,
        },
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == refill_history.id
    assert response_json["description"] == new_description
    assert response_json["event_type"] == new_event_type
    assert response_json["supply_id"] == supply2.id


def test_get_history_recharge_by_printer_id(client, refill_history: RefillHistory, printer: Printer):
    response = client.get(f"/api/v1/history/recharge?printer_id={printer.id}")
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(response_json["historys"]) > 0
    assert response_json["historys"][0]["printer_id"] == printer.id
    assert response_json["historys"][0]["id"] == refill_history.id


def test_delete_history_recharge(client, refill_history: RefillHistory):
    response = client.delete(f"/api/v1/history/recharge/{refill_history.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_history_recharge_not_found(client):
    response = client.delete("/api/v1/history/recharge/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND
