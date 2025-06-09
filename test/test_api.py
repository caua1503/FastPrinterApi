from http import HTTPStatus

def test_apirouter(client):
    response = client.get("/api/")

    assert response.status_code  == HTTPStatus.OK

def test_list_printers(client):
    response = client.get("/api/printers/")

    assert response.status_code == HTTPStatus.OK


def test_create_printer(client):
    
    dados_json = {
  "name": "string",
  "model": "string",
  "marca": "string",
  "ip": "string",
  "status": "string",
  "setor": "string",
  "descricao": "string",
  "previsao": "string",
  "insumo": "string",
  "ultima_recarga": "string",
  "ultima_manutencao": "string",
  "ultima_verificacao": "string"
}
    response = client.post("/api/printers/", 
                           json=dados_json)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
            "id": 1,
            "name": "string",
            "model": "string",
            "ip": "string",
            "marca": "string"
            }

