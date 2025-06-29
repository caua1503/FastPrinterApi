from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import has_access
from app.helpers.database_helper import get_session
from app.schemas.filter_schema import FilterPrinter, FilterPrinterHistory
from app.schemas.history_schema import (
    AlertHistorySchema,
    AlertHistorySchemaDB,
    ListAlertHistorySchema,
    ListMaintenanceHistorySchema,
    ListPrinterTrashHistorySchema,
    ListRefillHistorySchema,
    ListStatusHistorySchema,
    MaintenanceHistorySchema,
    MaintenanceHistorySchemaDB,
    PrinterTrashHistorySchema,
    PrinterTrashHistorySchemaDB,
    RefillHistorySchema,
    RefillHistorySchemaDB,
    StatusHistorySchema,
    StatusHistorySchemaDB,
)
from app.services.history_service import (
    create_history_maintenance,
    create_history_recharge,
    create_history_trash,
    delete_history_alert,
    delete_history_maintenance,
    delete_history_recharge,
    delete_history_status,
    delete_history_trash,
    get_history_alerts,
    get_history_maintenance,
    get_history_maintenance_id,
    get_history_recharge,
    get_history_recharge_id,
    get_history_status,
    get_history_status_id,
    get_history_trash,
    update_history_alert,
    update_history_maintenance,
    update_history_recharge,
    update_history_status,
    update_history_trash,
)

history_router = APIRouter()

"""
    Historys recharge
    /recharge: Retorna todos os históricos de recarga (GET, POST)
    /recharge/{id}: Retorna um histórico de recarga específico (GET, PUT, DELETE)
    /recharge/printer/{id}: Retorna um histórico de recarga de uma impressora específica (GET)
"""


@history_router.get("/recharge", status_code=HTTPStatus.OK, response_model=ListRefillHistorySchema)
async def api_get_history_recharge(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterPrinterHistory, Query()],
    current_user=has_access(),
):
    """
    Get all historys of recharge
    """
    result = await get_history_recharge(session, filters)
    return result


@history_router.post("/recharge", status_code=HTTPStatus.CREATED, response_model=RefillHistorySchemaDB)
async def api_create_history_recharge(
    history: RefillHistorySchema, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    """
    Create a new history of recharge
    """
    return await create_history_recharge(history, session)


@history_router.put("/recharge/{id}", status_code=HTTPStatus.OK, response_model=RefillHistorySchemaDB)
async def api_update_history_recharge(
    id: int,
    history: RefillHistorySchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(),
):
    """
    Update a history of recharge by id
    """
    return await update_history_recharge(id, history, session)


@history_router.get("/recharge/{id}", status_code=HTTPStatus.OK, response_model=Optional[RefillHistorySchemaDB])
async def api_get_history_recharge_id(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    """
    Get a history of recharge by id
    """
    return await get_history_recharge_id(id, session)


@history_router.delete("/recharge/{id}", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_history_recharge(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    """
    Delete a history of recharge by id
    """
    return await delete_history_recharge(id, session)


"""

    Historys maintenance

"""


@history_router.post("/maintenance", status_code=HTTPStatus.CREATED, response_model=MaintenanceHistorySchemaDB)
async def api_create_history_maintenance(
    history: MaintenanceHistorySchema, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    """
    Create a new history of maintenance
    """
    return await create_history_maintenance(history, session)


@history_router.get("/maintenance", status_code=HTTPStatus.OK, response_model=ListMaintenanceHistorySchema)
async def api_get_history_maintenance(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterPrinter, Query()],
    current_user=has_access(),
):
    """
    Get all historys of maintenance
    """
    result = await get_history_maintenance(session, filters)
    return result


@history_router.get("/maintenance/{id}", status_code=HTTPStatus.OK, response_model=MaintenanceHistorySchemaDB)
async def api_get_history_maintenance_id(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    """
    Get a history of maintenance by id
    """
    return await get_history_maintenance_id(id, session)


@history_router.put("/maintenance/{id}", status_code=HTTPStatus.OK, response_model=MaintenanceHistorySchemaDB)
async def api_update_history_maintenance(
    id: int,
    history: MaintenanceHistorySchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(),
):
    """
    Update a history of maintenance by id
    """
    return await update_history_maintenance(id, history, session)


@history_router.delete("/maintenance/{id}", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_history_maintenance(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    """
    Delete a history of maintenance by id
    """
    return await delete_history_maintenance(id, session)


"""

    Historys trash

"""


@history_router.get("/trash", status_code=HTTPStatus.OK, response_model=ListPrinterTrashHistorySchema)
async def api_get_history_trash(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterPrinter, Query()],
    current_user=has_access(),
):
    """
    Get all historys of trash
    """
    result = await get_history_trash(session, filters)
    return result


@history_router.put("/trash/{id}", status_code=HTTPStatus.OK, response_model=PrinterTrashHistorySchemaDB)
async def api_update_history_trash(
    id: int,
    history: PrinterTrashHistorySchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(),
):
    """
    Update a history of trash by id
    """
    return await update_history_trash(id, history, session)


@history_router.delete("/trash/{id}", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_history_trash(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    """
    Delete a history of trash by id
    """
    return await delete_history_trash(id, session)


@history_router.post("/trash", status_code=HTTPStatus.CREATED, response_model=PrinterTrashHistorySchemaDB)
async def api_create_history_trash(
    history: PrinterTrashHistorySchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(),
):
    """
    Create a new history of trash
    """
    return await create_history_trash(history, session)


@history_router.get("/alert", status_code=HTTPStatus.OK, response_model=ListAlertHistorySchema)
async def api_get_history_alerts(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterPrinter, Query()],
    current_user=has_access(),
):
    """
    Get all historys of alerts
    """
    result = await get_history_alerts(session, filters)
    return result


@history_router.put("/alert/{id}", status_code=HTTPStatus.OK, response_model=AlertHistorySchemaDB)
async def api_update_history_alert(
    id: int,
    history: AlertHistorySchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(),
):
    """
    Update a history of alert by id
    """
    return await update_history_alert(id, history, session)


@history_router.delete("/alert/{id}", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_history_alert(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    """
    Delete a history of alert by id
    """
    return await delete_history_alert(id, session)


"""

    Historys status

"""


@history_router.get("/status", status_code=HTTPStatus.OK, response_model=ListStatusHistorySchema)
async def api_get_history_status(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterPrinter, Query()],
    current_user=has_access(),
):
    """
    Get all historys of status
    """
    result = await get_history_status(session, filters)
    return result


@history_router.get("/status/{id}", status_code=HTTPStatus.OK, response_model=StatusHistorySchemaDB)
async def api_get_history_status_id(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    """
    Get a history of status by id
    """
    return await get_history_status_id(id, session)


@history_router.put("/status/{id}", status_code=HTTPStatus.OK, response_model=StatusHistorySchemaDB)
async def api_update_history_status(
    id: int, history: StatusHistorySchema, session: Annotated[AsyncSession, Depends(get_session)]
):
    """
    Update a history of status by id
    """
    return await update_history_status(id, history, session)


@history_router.delete("/status/{id}", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_history_status(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    """
    Delete a history of status by id
    """
    return await delete_history_status(id, session)
