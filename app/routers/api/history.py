from typing import List
from http import HTTPStatus
from fastapi import APIRouter
from models.history import  HistoryRecargaSchema ,HistoryRecargaSchemaDB, HistoryManutencaoSchema, HistoryManutencaoSchemaDB
from services.history_service import (get_history_recharge, create_history_recharge, 
                                      delete_history_recharge, update_history_recharge,
                                      get_history_maintenance, create_history_maintenance,
                                      delete_history_maintenance, update_history_maintenance)

history_router = APIRouter(prefix="/historys", tags=["historys"])

@history_router.get("/recharge", status_code=HTTPStatus.ACCEPTED)
async def api_get_history_recharge() -> List[HistoryRecargaSchemaDB]:
    ...

@history_router.get("/maintenance", status_code=HTTPStatus.ACCEPTED)
async def api_get_history_maintenance() -> List[HistoryManutencaoSchemaDB]:
    ...

@history_router.post("/recharge", status_code=HTTPStatus.CREATED,
                     response_model=HistoryRecargaSchema)
async def api_create_history_recharge():
    ...

@history_router.post("/maintenance", status_code=HTTPStatus.CREATED,
                     response_model=HistoryManutencaoSchema)
async def api_create_history_maintenance():
    ...

@history_router.get("/recharge/{id}", response_model=HistoryRecargaSchemaDB)
async def api_get_history_recharge_id(id:int):
    ...

@history_router.get("/maintenance/{id}", response_model=HistoryManutencaoSchemaDB)
async def api_get_history_maintenance_id(id:int):
    ...

@history_router.put("/recharge/{id}")
async def api_update_history_recharge(id:int):
    ...

@history_router.put("/maintenance/{id}")
async def api_update_history_maintenance(id:int):
    ...

@history_router.delete("/recharge/{id}")
async def api_delete_history_recharge(id:int):
    ...

@history_router.delete("/maintenance/{id}")
async def api_delete_history_maintenance(id:int):
    ...