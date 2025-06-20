from http import HTTPStatus

from app.models.printer_model import Printer, Status


def test_create_status(client):
    response = client.post(
        "/api/v1/status/",
        json={"status": "Test Status", "description": "Test Description"},
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["status"] == "Test Status"
    assert data["description"] == "Test Description"
    assert "id" in data


def test_get_status(client, status: Status):
    response = client.get("/api/v1/status/")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "status" in data
    assert len(data["status"]) == 1
    assert data["status"][0]["status"] == status.status
    assert data["status"][0]["description"] == status.description


def test_get_status_not_found(client):
    response = client.get("/api/v1/status/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_status_by_id(client, status: Status):
    response = client.get(f"/api/v1/status/{status.id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["status"] == status.status
    assert data["description"] == status.description


def test_get_status_by_id_not_found(client):
    response = client.get("/api/v1/status/999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_status(client, status: Status):
    response = client.put(
        f"/api/v1/status/{status.id}",
        json={"status": "Updated Status", "description": "Updated Description"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["status"] == "Updated Status"
    assert data["description"] == "Updated Description"


def test_update_status_not_found(client):
    response = client.put(
        "/api/v1/status/999",
        json={"status": "Updated Status", "description": "Updated Description"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_status(client, status: Status, printer: Printer):
    response = client.delete(f"/api/v1/printer/{printer.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT
    response = client.delete(f"/api/v1/status/{status.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_status_not_found(client):
    response = client.delete("/api/v1/status/999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_status_with_printer_associated(client, printer: Printer):
    response = client.delete(f"/api/v1/status/{printer.status_id}")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Status has printers"
