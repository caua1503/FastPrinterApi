from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.database_helper import get_session
from app.schemas.filters import FilterBase
from app.schemas.status_schema import StatusSchema
from app.services.status_service import create_status, delete_status, get_status, get_status_id, update_status

status_router = APIRouter()


@status_router.post("/", status_code=HTTPStatus.CREATED)
async def api_create_status(status: StatusSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    return await create_status(status, session)


@status_router.get("/", status_code=HTTPStatus.OK)
async def api_get_status(session: Annotated[AsyncSession, Depends(get_session)], filters: Annotated[FilterBase, Query()]):
    result = await get_status(session, filters)
    return {"status": result}


@status_router.put("/{id}", status_code=HTTPStatus.OK)
async def api_update_status(id: int, status: StatusSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    return await update_status(id, status, session)


@status_router.delete("/{id}", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_status(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await delete_status(id, session)


@status_router.get("/{id}", status_code=HTTPStatus.OK)
async def api_get_status_id(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_status_id(id, session)
