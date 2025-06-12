from http import HTTPStatus
from datetime import date
from sqlalchemy import select

def test_apirouter(client):
    response = client.get("/api/")

    assert response.status_code  == HTTPStatus.OK

def test_list_printers(client):
    response = client.get("/api/printers/")

    assert response.status_code == HTTPStatus.OK
    
def test_create_printer(client):
    dados_json = {
        "id_insumo": 1,
        "id_status": 1,
        "name": "string",
        "marca": "string",
        "model": "string",
        "ip": "192.168.1.100",
        "setor": "TI",
        "descricao": "Impressora de testes",
        "previsao": None,
        "ultima_recarga": None,
        "ultima_manutencao": None,
        "ultima_verificacao": None
    }
    response = client.post("/api/printers/", json=dados_json)

    assert response.status_code == HTTPStatus.CREATED
    assert "id" in response.json()
    assert response.json()["name"] == "string"
    assert response.json()["model"] == "string"
    assert response.json()["ip"] == "192.168.1.100"
    assert response.json()["marca"] == "string"

