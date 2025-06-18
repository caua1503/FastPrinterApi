from http import HTTPStatus
from datetime import date
import pytest

from app.models import Printer

def test_apirouter(client):
    response = client.get("/api/v1/")

    assert response.status_code == HTTPStatus.OK


def test_list_printers(client):
    response = client.get("/api/v1/printer/")

    assert response.status_code == HTTPStatus.OK  
