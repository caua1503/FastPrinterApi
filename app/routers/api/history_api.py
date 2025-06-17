from http import HTTPStatus
from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends
from helpers.db_helper import get_session
from schemas.history_schema import (
    HistoryAlertaSchema,
    HistoryAlertaSchemaDB,
    HistoryLixeiraSchema,
    HistoryLixeiraSchemaDB,
    HistoryManutencaoSchema,
    HistoryManutencaoSchemaDB,
    HistoryRecargaSchema,
    HistoryRecargaSchemaDB,
)
from services.history_service import (
    create_history_maintenance,
    create_history_recharge,
    create_history_trash,
    delete_history_alert,
    delete_history_maintenance,
    delete_history_recharge,
    delete_history_trash,
    get_history_alert,
    get_history_alert_printer_id,
    get_history_maintenance,
    get_history_maintenance_id,
    get_history_maintenance_printer_id,
    get_history_recharge,
    get_history_recharge_id,
    get_history_recharge_printer_id,
    get_history_trash,
    get_history_trash_printer_id,
    update_history_alert,
    update_history_maintenance,
    update_history_recharge,
    update_history_trash,
)
from sqlalchemy.ext.asyncio import AsyncSession

history_router = APIRouter(prefix="/historys", tags=["api - historys"])

"""
    Historys recharge
    /recharge: Retorna todos os históricos de recarga (GET, POST)
    /recharge/{id}: Retorna um histórico de recarga específico (GET, PUT, DELETE)
    /recharge/printer/{id}: Retorna um histórico de recarga de uma impressora específica (GET)
"""


@history_router.get("/recharge", status_code=HTTPStatus.ACCEPTED)
async def api_get_history_recharge(
    session: Annotated[AsyncSession, Depends(get_session)], limit: int = 10, offset: int = 0
) -> Dict[str, List[HistoryRecargaSchemaDB]]:
    result = await get_history_recharge(session, limit, offset)
    return {"historys": result}


@history_router.post("/recharge", status_code=HTTPStatus.CREATED, response_model=HistoryRecargaSchema)
async def api_create_history_recharge(
    history: HistoryRecargaSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> HistoryRecargaSchemaDB:
    return await create_history_recharge(history, session)


@history_router.put("/recharge/{id}")
async def api_update_history_recharge(
    id: int, history: HistoryRecargaSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> HistoryRecargaSchemaDB:
    return await update_history_recharge(id, history, session)


@history_router.get("/recharge/{id}")
async def api_get_history_recharge_id(
    id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> HistoryRecargaSchemaDB:
    return await get_history_recharge_id(id, session)


@history_router.get("/recharge/printer/{impressora_id}")
async def api_get_history_recharge_printer_id(
    session: Annotated[AsyncSession, Depends(get_session)], impressora_id: int, limit: int = 10, offset: int = 0
):
    result = await get_history_recharge_printer_id(impressora_id, limit, offset, session)
    return {"historys": result}


@history_router.delete("/recharge/{id}")
async def api_delete_history_recharge(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await delete_history_recharge(id, session)


"""

    Historys maintenance

"""


@history_router.post("/maintenance", status_code=HTTPStatus.CREATED, response_model=HistoryManutencaoSchema)
async def api_create_history_maintenance(
    history: HistoryManutencaoSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> HistoryManutencaoSchemaDB:
    return await create_history_maintenance(history, session)


@history_router.get("/maintenance", status_code=HTTPStatus.ACCEPTED)
async def api_get_history_maintenance(
    session: Annotated[AsyncSession, Depends(get_session)], limit: int = 10, offset: int = 0
) -> Dict[str, List[HistoryManutencaoSchemaDB]]:
    result = await get_history_maintenance(session, limit, offset)
    return {"historys": result}


@history_router.get("/maintenance/{id}", response_model=HistoryManutencaoSchemaDB)
async def api_get_history_maintenance_id(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_history_maintenance_id(id, session)


@history_router.get("/maintenance/printer/{impressora_id}")
async def api_get_history_maintenance_printer_id(
    session: Annotated[AsyncSession, Depends(get_session)], impressora_id: int, limit: int = 10, offset: int = 0
):
    result = await get_history_maintenance_printer_id(impressora_id, limit, offset, session)
    return {"historys": result}


@history_router.put("/maintenance/{id}")
async def api_update_history_maintenance(
    id: int, history: HistoryManutencaoSchema, session: Annotated[AsyncSession, Depends(get_session)]
):
    return await update_history_maintenance(id, history, session)


@history_router.delete("/maintenance/{id}")
async def api_delete_history_maintenance(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await delete_history_maintenance(id, session)


"""

    Historys trash

"""


@history_router.get("/trash", status_code=HTTPStatus.ACCEPTED)
async def api_get_history_trash(
    session: Annotated[AsyncSession, Depends(get_session)], limit: int = 10, offset: int = 0
) -> Dict[str, List[HistoryLixeiraSchemaDB]]:
    result = await get_history_trash(session, limit, offset)
    return {"historys": result}


@history_router.get("/trash/printer/{impressora_id}")
async def api_get_history_trash_printer_id(
    session: Annotated[AsyncSession, Depends(get_session)], impressora_id: int, limit: int = 10, offset: int = 0
):
    result = await get_history_trash_printer_id(impressora_id, limit, offset, session)
    return {"historys": result}


@history_router.put("/trash/{id}")
async def api_update_history_trash(
    id: int, history: HistoryLixeiraSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> HistoryLixeiraSchemaDB:
    return await update_history_trash(id, history, session)


@history_router.delete("/trash/{id}")
async def api_delete_history_trash(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await delete_history_trash(id, session)


@history_router.post("/trash", status_code=HTTPStatus.CREATED, response_model=HistoryLixeiraSchema)
async def api_create_history_trash(
    history: HistoryLixeiraSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> HistoryLixeiraSchemaDB:
    return await create_history_trash(history, session)


@history_router.get("/alert", status_code=HTTPStatus.ACCEPTED)
async def api_get_history_alert(
    session: Annotated[AsyncSession, Depends(get_session)], limit: int = 10, offset: int = 0
) -> Dict[str, List[HistoryAlertaSchemaDB]]:
    result = await get_history_alert(session, limit, offset)
    return {"historys": result}


@history_router.get("/alert/{impressora_id}", response_model=HistoryAlertaSchemaDB)
async def api_get_history_alert_printer_id(
    session: Annotated[AsyncSession, Depends(get_session)], impressora_id: int, limit: int = 10, offset: int = 0
):
    result = await get_history_alert_printer_id(impressora_id, limit, offset, session)
    return {"historys": result}


@history_router.put("/alert/{id}")
async def api_update_history_alert(
    id: int, history: HistoryAlertaSchema, session: Annotated[AsyncSession, Depends(get_session)]
):
    return await update_history_alert(id, history, session)


@history_router.delete("/alert/{id}")
async def api_delete_history_alert(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await delete_history_alert(id, session)
