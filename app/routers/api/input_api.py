from http import HTTPStatus
from fastapi import APIRouter
from models.input_model import InputSchema, TipoInsumoSchema
from fastapi import Depends
from sqlalchemy.orm import Session
from helpers.db_helper import get_session
from services.input_service import (create_input, get_input, get_input_id, 
                                    update_input, delete_input, get_input_type, 
                                    create_input_type, update_input_type, delete_input_type, 
                                    get_input_type_id)

input_router = APIRouter(prefix="/input", tags=["input"])

@input_router.post("/", status_code=HTTPStatus.CREATED)
async def api_create_input(input: InputSchema, session: Session = Depends(get_session)):
    return await create_input(input, session)

@input_router.get("/")
async def api_get_input(session: Session = Depends(get_session), limit: int = 10, offset: int = 0):
    result = await get_input(session, limit, offset)
    return {"inputs": result}

@input_router.get("/{id}")
async def api_get_input_id(id: int, session: Session = Depends(get_session)):
    return await get_input_id(id, session)

@input_router.put("/{id}")
async def api_update_input(id: int, input: InputSchema, session: Session = Depends(get_session)):
    return await update_input(id, input, session)

@input_router.delete("/{id}")
async def api_delete_input(id: int, session: Session = Depends(get_session)):
    return await delete_input(id, session)

@input_router.get("/type")
async def api_get_input_type(session: Session = Depends(get_session)):
    result = await get_input_type(session)
    return {"input_types": result}

@input_router.post("/type")
async def api_create_input_type(input_type: TipoInsumoSchema, session: Session = Depends(get_session)):
    return await create_input_type(input_type, session)

@input_router.put("/type/{id}")
async def api_update_input_type(id: int, input_type: TipoInsumoSchema, session: Session = Depends(get_session)):
    return await update_input_type(id, input_type, session)

@input_router.delete("/type/{id}")
async def api_delete_input_type(id: int, session: Session = Depends(get_session)):
    return await delete_input_type(id, session)

@input_router.get("/type/{id}")
async def api_get_input_type_id(id: int, session: Session = Depends(get_session)):
    return await get_input_type_id(id, session)