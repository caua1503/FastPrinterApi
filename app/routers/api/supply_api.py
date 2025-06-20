from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.database_helper import get_session
from app.schemas.filters import FilterBase
from app.schemas.supply_schema import SupplySchema, SupplyTypeSchema
from app.services.supply_service import (
    create_supply,
    create_supply_type,
    delete_supply,
    delete_supply_type,
    get_supply,
    get_supply_id,
    get_supply_type,
    get_supply_type_id,
    update_supply,
    update_supply_type,
)

supply_router = APIRouter()


@supply_router.post("/", status_code=HTTPStatus.CREATED)
async def api_create_supply(supply: SupplySchema, session: Annotated[AsyncSession, Depends(get_session)]):
    return await create_supply(supply, session)


@supply_router.get("/")
async def api_get_supply(session: Annotated[AsyncSession, Depends(get_session)], filters: Annotated[FilterBase, Query()]):
    result = await get_supply(session, filters)
    return {"supplys": result}


@supply_router.get("/{id}")
async def api_get_supply_id(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_supply_id(id, session)


@supply_router.put("/{id}")
async def api_update_supply(id: int, supply: SupplySchema, session: Annotated[AsyncSession, Depends(get_session)]):
    return await update_supply(id, supply, session)


@supply_router.delete("/{id}")
async def api_delete_supply(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await delete_supply(id, session)


@supply_router.get("/type")
async def api_get_supply_type(session: Annotated[AsyncSession, Depends(get_session)]):
    result = await get_supply_type(session)
    return {"supply_types": result}


@supply_router.post("/type")
async def api_create_supply_type(supply_type: SupplyTypeSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    return await create_supply_type(supply_type, session)


@supply_router.put("/type/{id}")
async def api_update_supply_type(
    id: int, supply_type: SupplyTypeSchema, session: Annotated[AsyncSession, Depends(get_session)]
):
    return await update_supply_type(id, supply_type, session)


@supply_router.delete("/type/{id}")
async def api_delete_supply_type(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await delete_supply_type(id, session)


@supply_router.get("/type/{id}")
async def api_get_supply_type_id(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_supply_type_id(id, session)
