from http import HTTPStatus
from fastapi import APIRouter
from models.status_model import StatusSchema
from fastapi import Depends
from sqlalchemy.orm import Session
from helpers.db_helper import get_session
from services.status_service import (create_status, get_status, get_status_id, 
                                    update_status, delete_status)

status_router = APIRouter(prefix="/status", tags=["status"])

@status_router.post("/", status_code=HTTPStatus.CREATED)
async def api_create_status(status: StatusSchema, session: Session = Depends(get_session)):
    return await create_status(status, session)

@status_router.get("/")
async def api_get_status(session: Session = Depends(get_session)):
    result = await get_status(session)
    return {"status": result}

@status_router.put("/{id}")
async def api_update_status(id: int, status: StatusSchema, session: Session = Depends(get_session)):
    return await update_status(id, status, session)

@status_router.delete("/{id}")
async def api_delete_status(id: int, session: Session = Depends(get_session)):
    return await delete_status(id, session)

@status_router.get("/{id}")
async def api_get_status_id(id: int, session: Session = Depends(get_session)):
    return await get_status_id(id, session)