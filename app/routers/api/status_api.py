from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from helpers.database_helper import get_session
from schemas.status_schema import StatusSchema
from services.status_service import create_status, delete_status, get_status, get_status_id, update_status
from sqlalchemy.ext.asyncio import AsyncSession

status_router = APIRouter()


@status_router.post("/", status_code=HTTPStatus.CREATED)
async def api_create_status(status: StatusSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    return await create_status(status, session)


@status_router.get("/")
async def api_get_status(session: Annotated[AsyncSession, Depends(get_session)]):
    result = await get_status(session)
    return {"status": result}


@status_router.put("/{id}")
async def api_update_status(id: int, status: StatusSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    return await update_status(id, status, session)


@status_router.delete("/{id}")
async def api_delete_status(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await delete_status(id, session)


@status_router.get("/{id}")
async def api_get_status_id(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_status_id(id, session)
