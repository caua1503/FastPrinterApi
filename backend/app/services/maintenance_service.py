from datetime import date
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.config import get_config
from app.helpers.maintenance_helper import (
    calculate_next_recharge,
    calculate_recharge_percentage,
    calculate_trash_cleaning_next_time,
    calculate_trash_cleaning_percentage,
)
from app.models.history_model import AlertHistory, MaintenanceInfoHistory, PrinterTrashHistory, RefillHistory
from app.models.maintenance_model import PrinterMaintenanceInfo
from app.models.printer_model import Printer
from app.schemas.filter_schema import FilterBase
from app.schemas.history_schema import AlertHistorySchema

config = get_config()

TRASH_ALERT_THRESHOLD = 90


async def create_history_alert_core(history: AlertHistorySchema, session: AsyncSession) -> AlertHistorySchema:
    history_db = AlertHistory(
        printer_id=history.printer_id,
        date=history.date,
        alert_type=history.alert_type,
        description=history.description,
    )

    session.add(history_db)
    await session.commit()
    await session.refresh(history_db)

    return AlertHistorySchema(
        printer_id=history_db.printer_id,
        date=history_db.date,
        alert_type=history_db.alert_type,
        description=history_db.description,
    )


async def extract_dates_recharge(printer_id: int, session: AsyncSession, filters: FilterBase) -> List:
    history_recharge = (
        await session.scalars(
            select(RefillHistory)
            .where(RefillHistory.printer_id == printer_id)
            .order_by(RefillHistory.date.desc())
            .limit(filters.limit)
        )
    ).all()
    if history_recharge:
        return [recharge.date for recharge in history_recharge]
    else:
        return []


async def extract_trash_dates(printer_id: int, session: AsyncSession, filters: FilterBase) -> List:
    history_trash = (
        await session.scalars(
            select(PrinterTrashHistory)
            .where(PrinterTrashHistory.printer_id == printer_id)
            .order_by(PrinterTrashHistory.date.desc())
            .limit(filters.limit)
        )
    ).all()
    if history_trash:
        return [trash.date for trash in history_trash]
    else:
        return []


async def get_all_printers_maintenance_info(session: AsyncSession, filters: FilterBase):
    """
    Atualiza as informações de manutenção para todas as impressoras.
    Processa todas as impressoras em uma única transação para manter atomicidade.

    Args:
        session (AsyncSession): Sessão do banco de dados.
        filters (FilterBase): Filtros para análise histórica.

    Returns:
        None: A função atualiza os dados no banco, não retorna valores.
    """
    try:
        batch_size = config.PRINTER_MAINTENANCE_BATCH_SIZE
        objects_to_add = []
        query = select(Printer)

        async for printer in await session.stream_scalars(query):
            datas_recarga = await extract_dates_recharge(printer.id, session, filters)
            trash_datas = await extract_trash_dates(printer.id, session, filters)

            if datas_recarga:
                next_recharge_date = calculate_next_recharge(datas_recarga, "media")
                percentage = calculate_recharge_percentage(datas_recarga)
            else:
                next_recharge_date = None
                percentage = 0.0

            trash_cleaning_next_time_date = calculate_trash_cleaning_next_time(trash_datas)
            trash_cleaning_percentage_value = calculate_trash_cleaning_percentage(trash_datas)

            if trash_cleaning_percentage_value >= TRASH_ALERT_THRESHOLD:
                alert_description = f"A limpeza da lixeira é urgente, percentual: {trash_cleaning_percentage_value}%"
                alert_history = AlertHistorySchema(
                    printer_id=printer.id,
                    date=date.today(),
                    alert_type="limpeza_urgente",
                    description=alert_description,
                )
                await create_history_alert_core(alert_history, session)

            exist_maintenance_info = await session.scalar(
                select(PrinterMaintenanceInfo).where(PrinterMaintenanceInfo.printer_id == printer.id)
            )

            history_recharge = MaintenanceInfoHistory(
                printer_id=printer.id,
                refill_percentage=percentage,
                cleaning_percentage=trash_cleaning_percentage_value,
            )
            objects_to_add.append(history_recharge)

            if exist_maintenance_info:
                exist_maintenance_info.next_refill = next_recharge_date
                exist_maintenance_info.refill_percentage = percentage
                exist_maintenance_info.cleaning_percentage = trash_cleaning_percentage_value
                exist_maintenance_info.next_cleaning = trash_cleaning_next_time_date
                exist_maintenance_info.last_update = date.today()
            else:
                new_maintenance_info = PrinterMaintenanceInfo(
                    printer_id=printer.id,
                    last_update=date.today(),
                    refill_percentage=percentage,
                    cleaning_percentage=trash_cleaning_percentage_value,
                    next_refill=next_recharge_date,
                    next_cleaning=trash_cleaning_next_time_date,
                )
                objects_to_add.append(new_maintenance_info)

            if len(objects_to_add) >= batch_size:
                session.add_all(objects_to_add)
                objects_to_add.clear()

        if objects_to_add:
            session.add_all(objects_to_add)

        await session.commit()

    except Exception as e:
        await session.rollback()
        raise e


async def get_printer_maintenance_info(printer_id: int, session: AsyncSession, filters: FilterBase):
    """
    Retorna um dicionário com as informações de manutenção da impressora.
    Args:
        printer_id (int): ID da impressora.
        session (AsyncSession): Sessão do banco de dados.
        filters (FilterBase): Filtros para análise histórica.
    Returns:
        dict: Dicionário com:
            - id (int): ID da impressora
            - next_recharge (date | None): Próxima data de recarga como objeto date ou None
            - percentage (float): Percentual de carga atual (0.0-100.0)
            - trash_cleaning_next_time (date | None): Próxima data de limpeza da lixeira como objeto date ou None
            - trash_cleaning_percentage (float): Percentual de necessidade de limpeza da lixeira (0.0-100.0)
    """
    datas_recarga = await extract_dates_recharge(printer_id, session, filters)
    trash_datas = await extract_trash_dates(printer_id, session, filters)

    if datas_recarga:
        next_recharge_date = calculate_next_recharge(datas_recarga, "media")
        percentage = calculate_recharge_percentage(datas_recarga)
    else:
        next_recharge_date = None
        percentage = 0.0

    trash_cleaning_next_time_date = calculate_trash_cleaning_next_time(trash_datas)
    trash_cleaning_percentage_value = calculate_trash_cleaning_percentage(trash_datas)

    return {
        "id": printer_id,
        "next_recharge": next_recharge_date,
        "percentage": percentage,
        "trash_cleaning_next_time": trash_cleaning_next_time_date,
        "trash_cleaning_percentage": trash_cleaning_percentage_value,
    }


async def get_printer_maintenance_info_service(printer_id: int, session: AsyncSession, filters: FilterBase) -> dict:
    printer = await session.scalar(select(Printer).where(Printer.id == printer_id))
    if not printer:
        raise HTTPException(status_code=404, detail="Impressora não encontrada")

    info_manutencao = await session.scalar(
        select(PrinterMaintenanceInfo).where(PrinterMaintenanceInfo.printer_id == printer_id)
    )
    hoje = date.today()

    if info_manutencao:
        if info_manutencao.last_update != hoje:
            info_dict = await get_printer_maintenance_info(printer_id, session, filters)
            info_manutencao.last_update = hoje
            info_manutencao.next_refill = info_dict["next_recharge"]
            info_manutencao.refill_percentage = info_dict["percentage"]
            info_manutencao.next_cleaning = info_dict["trash_cleaning_next_time"]
            info_manutencao.cleaning_percentage = info_dict["trash_cleaning_percentage"]
            await session.commit()
        return {
            "id": printer_id,
            "next_recharge": info_manutencao.next_refill.strftime("%d/%m/%Y") if info_manutencao.next_refill else "N/A",
            "percentage": info_manutencao.refill_percentage,
            "trash_cleaning_next_time": info_manutencao.next_cleaning.strftime("%d/%m/%Y")
            if info_manutencao.next_cleaning
            else "N/A",
            "trash_cleaning_percentage": f"{info_manutencao.cleaning_percentage:.2f}%",
        }
    else:
        info_dict = await get_printer_maintenance_info(printer_id, session, filters)
        novo_info = PrinterMaintenanceInfo(
            printer_id=printer_id,
            last_update=hoje,
            next_refill=info_dict["next_recharge"],
            refill_percentage=info_dict["percentage"],
            next_cleaning=info_dict["trash_cleaning_next_time"],
            cleaning_percentage=info_dict["trash_cleaning_percentage"],
        )
        session.add(novo_info)
        await session.commit()
        return {
            "id": printer_id,
            "next_recharge": novo_info.next_refill.strftime("%d/%m/%Y") if novo_info.next_refill else "N/A",
            "percentage": novo_info.refill_percentage,
            "trash_cleaning_next_time": novo_info.next_cleaning.strftime("%d/%m/%Y")
            if novo_info.next_cleaning
            else "N/A",
            "trash_cleaning_percentage": f"{novo_info.cleaning_percentage:.2f}%",
        }
