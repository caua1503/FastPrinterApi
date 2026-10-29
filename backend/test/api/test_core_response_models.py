from http import HTTPStatus

import pytest

from app.main import app
from app.models.department_model import Department
from app.models.printer_model import Printer, Status
from app.models.supply_model import Supply, SupplyType
from app.schemas.department_schema import DepartmentListResponse, DepartmentSchemaDB
from app.schemas.printer_schema import FullPrinterPublicSchema, FullPrinterSchemaDB
from app.schemas.status_schema import StatusListResponse, StatusSchemaDB
from app.schemas.supply_schema import SupplyListResponse, SupplySchemaDB, SupplyTypeListResponse, SupplyTypeSchemaDB


def test_routes_response_model_configured():
    route_map = {}
    for route in app.routes:
        if hasattr(route, "endpoint") and hasattr(route, "response_model"):
            route_map[(route.path, tuple(route.methods))] = route.response_model

    assert route_map.get(("/api/v1/printer/{id}", ("GET",))) == FullPrinterPublicSchema
    assert route_map.get(("/api/v1/printer/{id}", ("PUT",))) == FullPrinterSchemaDB

    assert route_map.get(("/api/v1/status/", ("GET",))) == StatusListResponse
    assert route_map.get(("/api/v1/status/", ("POST",))) == StatusSchemaDB
    assert route_map.get(("/api/v1/status/{id}", ("GET",))) == StatusSchemaDB
    assert route_map.get(("/api/v1/status/{id}", ("PUT",))) == StatusSchemaDB

    assert route_map.get(("/api/v1/supply/", ("GET",))) == SupplyListResponse
    assert route_map.get(("/api/v1/supply/", ("POST",))) == SupplySchemaDB
    assert route_map.get(("/api/v1/supply/{id}", ("GET",))) == SupplySchemaDB
    assert route_map.get(("/api/v1/supply/{id}", ("PUT",))) == SupplySchemaDB
    assert route_map.get(("/api/v1/supply/type", ("GET",))) == SupplyTypeListResponse
    assert route_map.get(("/api/v1/supply/type", ("POST",))) == SupplyTypeSchemaDB
    assert route_map.get(("/api/v1/supply/type/{id}", ("GET",))) == SupplyTypeSchemaDB
    assert route_map.get(("/api/v1/supply/type/{id}", ("PUT",))) == SupplyTypeSchemaDB

    assert route_map.get(("/api/v1/department/", ("GET",))) == DepartmentListResponse
    assert route_map.get(("/api/v1/department/", ("POST",))) == DepartmentSchemaDB
    assert route_map.get(("/api/v1/department/{id}", ("GET",))) == DepartmentSchemaDB
    assert route_map.get(("/api/v1/department/{id}", ("PUT",))) == DepartmentSchemaDB


@pytest.mark.asyncio
async def test_printer_id_response_model(client, printer: Printer, member_token):
    res_get = client.get(f"/api/v1/printer/{printer.id}", headers={"Authorization": f"Bearer {member_token}"})
    assert res_get.status_code == HTTPStatus.OK
    parsed_get = FullPrinterPublicSchema.model_validate(res_get.json())
    assert parsed_get.id == printer.id

    res_put = client.put(
        f"/api/v1/printer/{printer.id}",
        json={"name": "Printer Updated"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert res_put.status_code == HTTPStatus.OK
    parsed_put = FullPrinterSchemaDB.model_validate(res_put.json())
    assert parsed_put.name == "Printer Updated"


@pytest.mark.asyncio
async def test_status_response_models(client, status: Status, member_token):
    # GET list
    res_list = client.get("/api/v1/status/", headers={"Authorization": f"Bearer {member_token}"})
    assert res_list.status_code == HTTPStatus.OK
    parsed_list = StatusListResponse.model_validate(res_list.json())
    assert len(parsed_list.status) >= 1

    # POST create
    res_post = client.post(
        "/api/v1/status/",
        json={"status": "New Status", "description": "Desc"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert res_post.status_code == HTTPStatus.CREATED
    parsed_post = StatusSchemaDB.model_validate(res_post.json())
    assert parsed_post.status == "New Status"

    # GET by id
    res_get = client.get(f"/api/v1/status/{status.id}", headers={"Authorization": f"Bearer {member_token}"})
    assert res_get.status_code == HTTPStatus.OK
    parsed_get = StatusSchemaDB.model_validate(res_get.json())
    assert parsed_get.id == status.id

    # PUT by id
    res_put = client.put(
        f"/api/v1/status/{status.id}",
        json={"status": "Status Mod", "description": "Desc Mod"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert res_put.status_code == HTTPStatus.OK
    parsed_put = StatusSchemaDB.model_validate(res_put.json())
    assert parsed_put.status == "Status Mod"


@pytest.mark.asyncio
async def test_supply_response_models(client, supply: Supply, supply_type: SupplyType, member_token):  # noqa: PLR0914
    # GET list
    res_list = client.get("/api/v1/supply/", headers={"Authorization": f"Bearer {member_token}"})
    assert res_list.status_code == HTTPStatus.OK
    parsed_list = SupplyListResponse.model_validate(res_list.json())
    assert len(parsed_list.supplys) >= 1

    # POST create
    res_post = client.post(
        "/api/v1/supply/",
        json={"name": "New Supply", "supply_type_id": supply_type.id, "brand": "Brand", "description": "Desc"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert res_post.status_code == HTTPStatus.CREATED
    parsed_post = SupplySchemaDB.model_validate(res_post.json())
    assert parsed_post.name == "New Supply"

    # GET by id
    res_get = client.get(f"/api/v1/supply/{supply.id}", headers={"Authorization": f"Bearer {member_token}"})
    assert res_get.status_code == HTTPStatus.OK
    parsed_get = SupplySchemaDB.model_validate(res_get.json())
    assert parsed_get.id == supply.id

    # PUT by id
    res_put = client.put(
        f"/api/v1/supply/{supply.id}",
        json={"name": "Supply Mod", "supply_type_id": supply_type.id, "brand": "Brand Mod", "description": "Desc"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert res_put.status_code == HTTPStatus.OK
    parsed_put = SupplySchemaDB.model_validate(res_put.json())
    assert parsed_put.name == "Supply Mod"

    # GET type list
    res_t_list = client.get("/api/v1/supply/type", headers={"Authorization": f"Bearer {member_token}"})
    assert res_t_list.status_code == HTTPStatus.OK
    parsed_t_list = SupplyTypeListResponse.model_validate(res_t_list.json())
    assert len(parsed_t_list.supply_types) >= 1

    # POST type create
    res_t_post = client.post(
        "/api/v1/supply/type",
        json={"name": "New Supply Type"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert res_t_post.status_code == HTTPStatus.CREATED
    parsed_t_post = SupplyTypeSchemaDB.model_validate(res_t_post.json())
    assert parsed_t_post.name == "New Supply Type"

    # GET type by id
    res_t_get = client.get(f"/api/v1/supply/type/{supply_type.id}", headers={"Authorization": f"Bearer {member_token}"})
    assert res_t_get.status_code == HTTPStatus.OK
    parsed_t_get = SupplyTypeSchemaDB.model_validate(res_t_get.json())
    assert parsed_t_get.id == supply_type.id

    # PUT type by id
    res_t_put = client.put(
        f"/api/v1/supply/type/{supply_type.id}",
        json={"name": "Supply Type Mod"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert res_t_put.status_code == HTTPStatus.OK
    parsed_t_put = SupplyTypeSchemaDB.model_validate(res_t_put.json())
    assert parsed_t_put.name == "Supply Type Mod"


@pytest.mark.asyncio
async def test_department_response_models(client, department: Department, member_token):
    # GET list
    res_list = client.get("/api/v1/department/", headers={"Authorization": f"Bearer {member_token}"})
    assert res_list.status_code == HTTPStatus.OK
    parsed_list = DepartmentListResponse.model_validate(res_list.json())
    assert len(parsed_list.departments) >= 1

    # POST create
    res_post = client.post(
        "/api/v1/department/",
        json={"name": "New Dept", "description": "Dept Desc"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert res_post.status_code == HTTPStatus.OK
    parsed_post = DepartmentSchemaDB.model_validate(res_post.json())
    assert parsed_post.name == "New Dept"

    # GET by id
    res_get = client.get(f"/api/v1/department/{department.id}", headers={"Authorization": f"Bearer {member_token}"})
    assert res_get.status_code == HTTPStatus.OK
    parsed_get = DepartmentSchemaDB.model_validate(res_get.json())
    assert parsed_get.id == department.id

    # PUT by id
    res_put = client.put(
        f"/api/v1/department/{department.id}",
        json={"name": "Dept Mod", "description": "Desc Mod"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert res_put.status_code == HTTPStatus.OK
    parsed_put = DepartmentSchemaDB.model_validate(res_put.json())
    assert parsed_put.name == "Dept Mod"
