from datetime import date
from http import HTTPStatus

import pytest

from app.models.history_model import RefillHistory
from app.models.printer_model import Printer
from app.models.supply_model import Supply


@pytest.mark.asyncio
async def test_get_history_recharge_empty(client, token):
    response = client.get("/api/v1/history/recharge", headers={"Authorization": f"Bearer {token}"})
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"historys": [], "total": 0, "count": 0}


@pytest.mark.asyncio
async def test_get_history_recharge(client, refill_history: RefillHistory, token):
    response = client.get("/api/v1/history/recharge", headers={"Authorization": f"Bearer {token}"})
    print(response.json())
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert response_json["historys"][0]["id"] == refill_history.id
    assert response_json["historys"][0]["printer_id"] == refill_history.printer_id
    assert response_json["historys"][0]["date"] == refill_history.date.strftime("%Y-%m-%d")
    assert response_json["historys"][0]["event_type"] == refill_history.event_type
    assert response_json["historys"][0]["supply_id"] == refill_history.supply_id
    assert response_json["historys"][0]["description"] == refill_history.description


@pytest.mark.asyncio
async def test_get_history_recharge_by_id(client, refill_history: RefillHistory, token):
    response = client.get(f"/api/v1/history/recharge/{refill_history.id}", headers={"Authorization": f"Bearer {token}"})
    print(response.json())
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["id"] == refill_history.id
    assert response_json["printer_id"] == refill_history.printer_id
    assert response_json["date"] == refill_history.date.strftime("%Y-%m-%d")
    assert response_json["event_type"] == refill_history.event_type
    assert response_json["supply_id"] == refill_history.supply_id
    assert response_json["description"] == refill_history.description


@pytest.mark.asyncio
async def test_create_history_recharge(client, printer: Printer, supply: Supply, token):
    response = client.post(
        "/api/v1/history/recharge",
        json={
            "printer_id": printer.id,
            "date": date.today().strftime("%Y-%m-%d"),
            "event_type": "Test Recharge",
            "supply_id": supply.id,
            "description": "Test description",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json["printer_id"] == printer.id
    assert response_json["supply_id"] == supply.id
    assert response_json["description"] == "Test description"
    assert "id" in response_json


@pytest.mark.asyncio
async def test_update_history_recharge(client, refill_history: RefillHistory, supply2: Supply, token):
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
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == refill_history.id
    assert response_json["description"] == new_description
    assert response_json["event_type"] == new_event_type
    assert response_json["supply_id"] == supply2.id


@pytest.mark.asyncio
async def test_get_history_recharge_by_printer_id(client, refill_history: RefillHistory, printer: Printer, token):
    response = client.get(
        f"/api/v1/history/recharge?printer_id={printer.id}", headers={"Authorization": f"Bearer {token}"}
    )
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert len(response_json["historys"]) > 0
    assert response_json["historys"][0]["printer_id"] == printer.id
    assert response_json["historys"][0]["id"] == refill_history.id


@pytest.mark.asyncio
async def test_delete_history_recharge(client, refill_history: RefillHistory, token):
    response = client.delete(
        f"/api/v1/history/recharge/{refill_history.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_history_recharge_not_found(client, token):
    response = client.delete("/api/v1/history/recharge/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND
