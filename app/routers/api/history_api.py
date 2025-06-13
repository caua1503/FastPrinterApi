from typing import List, Dict
from http import HTTPStatus
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from helpers.db_helper import get_session
from models.history_model import  (HistoryRecargaSchema ,HistoryRecargaSchemaDB, 
                             HistoryManutencaoSchema, HistoryManutencaoSchemaDB)
from services.history_service import (get_history_recharge, get_history_recharge_id, get_history_recharge_printer_id, 
                                      create_history_recharge, update_history_recharge, delete_history_recharge,
                                      get_history_maintenance, get_history_maintenance_id, get_history_maintenance_printer_id, 
                                      create_history_maintenance, update_history_maintenance, delete_history_maintenance)

history_router = APIRouter(prefix="/historys", tags=["historys"])

"""
    Historys recharge
    /recharge: Retorna todos os históricos de recarga (GET, POST)
    /recharge/{id}: Retorna um histórico de recarga específico (GET, PUT, DELETE)
    /recharge/printer/{id}: Retorna um histórico de recarga de uma impressora específica (GET)
"""

@history_router.get("/recharge", status_code=HTTPStatus.ACCEPTED)
async def api_get_history_recharge(session: Session = Depends(get_session), 
                                   limit: int = 10, offset: int = 0
                                   ) -> Dict[str, List[HistoryRecargaSchemaDB]]:
    result = await get_history_recharge(session, limit, offset)
    return {"historys": result}

@history_router.post("/recharge", status_code=HTTPStatus.CREATED,
                     response_model=HistoryRecargaSchema)
async def api_create_history_recharge(history: HistoryRecargaSchema, 
                                      session: Session = Depends(get_session)
                                      ) -> HistoryRecargaSchemaDB:
    return await create_history_recharge(history, session)

@history_router.put("/recharge/{id}")
async def api_update_history_recharge(id:int, history: HistoryRecargaSchema, 
                                      session: Session = Depends(get_session)
                                      ) -> HistoryRecargaSchemaDB:
    return await update_history_recharge(id, history, session)

@history_router.get("/recharge/{id}", response_model=HistoryRecargaSchemaDB)
async def api_get_history_recharge_id(id:int, session: Session = Depends(get_session)
                                      ) -> HistoryRecargaSchemaDB:
    return await get_history_recharge_id(id, session)

@history_router.get("/recharge/printer/{impressora_id}")
async def api_get_history_recharge_printer_id(impressora_id:int, limit: int = 10, 
                                              offset: int = 0, session: Session = Depends(get_session)
                                              ):
    result = await get_history_recharge_printer_id(impressora_id, limit, offset, session)
    return {"historys": result}

@history_router.delete("/recharge/{id}")
async def api_delete_history_recharge(id:int, session: Session = Depends(get_session)):
    return await delete_history_recharge(id, session)

"""

    Historys maintenance

"""

@history_router.post("/maintenance", status_code=HTTPStatus.CREATED,
                     response_model=HistoryManutencaoSchema)
async def api_create_history_maintenance(history: HistoryManutencaoSchema, 
                                         session: Session = Depends(get_session)
                                         ) -> HistoryManutencaoSchemaDB:
    return await create_history_maintenance(history, session)

@history_router.get("/maintenance", status_code=HTTPStatus.ACCEPTED)
async def api_get_history_maintenance(session: Session = Depends(get_session), 
                                      limit: int = 10, offset: int = 0
                                      ) -> Dict[str, List[HistoryManutencaoSchemaDB]]:
    result = await get_history_maintenance(session, limit, offset)
    return {"historys": result}


@history_router.get("/maintenance/{id}", response_model=HistoryManutencaoSchemaDB)
async def api_get_history_maintenance_id(id:int, session: Session = Depends(get_session)):
    return await get_history_maintenance_id(id, session)

@history_router.get("/maintenance/printer/{impressora_id}")
async def api_get_history_maintenance_printer_id(impressora_id:int, limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    result = await get_history_maintenance_printer_id(impressora_id, limit, offset, session)
    return {"historys": result}

@history_router.put("/maintenance/{id}")
async def api_update_history_maintenance(id:int, history: HistoryManutencaoSchema, 
                                         session: Session = Depends(get_session)):
    return await update_history_maintenance(id, history, session)

@history_router.delete("/maintenance/{id}")
async def api_delete_history_maintenance(id:int, session: Session = Depends(get_session)):
    return await delete_history_maintenance(id, session)