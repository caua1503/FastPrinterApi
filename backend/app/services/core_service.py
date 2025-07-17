from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_printer_maintenance_info
from app.models.maintenance_model import PrinterMaintenanceInfo
from app.models.printer_model import Printer
from app.schemas.filter_schema import FilterBase


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
