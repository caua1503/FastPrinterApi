from datetime import date
from http import HTTPStatus

import pytest

from app.models.history_model import PrinterTrashHistory
from app.models.printer_model import Printer


@pytest.mark.asyncio
async def test_get_history_trash_empty(client, token):
    response = client.get("/api/v1/history/trash", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"historys": [], "total": 0, "count": 0}


@pytest.mark.asyncio
async def test_get_history_trash(client, printer_trash_history: PrinterTrashHistory, token):
    response = client.get("/api/v1/history/trash", headers={"Authorization": f"Bearer {token}"})
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert response_json["historys"][0]["id"] == printer_trash_history.id
    assert response_json["historys"][0]["printer_id"] == printer_trash_history.printer_id
    assert response_json["historys"][0]["date"] == printer_trash_history.date.strftime("%Y-%m-%d")
    assert response_json["historys"][0]["description"] == printer_trash_history.description


@pytest.mark.asyncio
async def test_create_history_trash(client, printer: Printer, token):
    response = client.post(
        "/api/v1/history/trash",
        json={
            "printer_id": printer.id,
            "date": date.today().strftime("%Y-%m-%d"),
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
async def test_update_history_trash(client, printer_trash_history: PrinterTrashHistory, token):
    new_description = "Updated description"
    response = client.put(
        f"/api/v1/history/trash/{printer_trash_history.id}",
        json={
            "printer_id": printer_trash_history.printer_id,
            "date": date.today().strftime("%Y-%m-%d"),
            "description": new_description,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == printer_trash_history.id
    assert response_json["description"] == new_description


@pytest.mark.asyncio
async def test_get_history_trash_by_printer_id(
    client, printer_trash_history: PrinterTrashHistory, printer: Printer, token
):
    response = client.get(
        f"/api/v1/history/trash?printer_id={printer.id}", headers={"Authorization": f"Bearer {token}"}
    )
    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["total"] == 1
    assert response_json["count"] == 1
    assert len(response_json["historys"]) > 0
    assert response_json["historys"][0]["printer_id"] == printer.id
    assert response_json["historys"][0]["id"] == printer_trash_history.id


@pytest.mark.asyncio
async def test_delete_history_trash(client, printer_trash_history: PrinterTrashHistory, token):
    response = client.delete(
        f"/api/v1/history/trash/{printer_trash_history.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_history_trash_not_found(client, token):
    response = client.delete("/api/v1/history/trash/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND
