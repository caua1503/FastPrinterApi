from datetime import date

from core import get_printer_maintenance_info
from fastapi import HTTPException
from models.model_db import Impressora, Info_Manutencao_Impressora
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_printer_maintenance_info_service(printer_id: int, session: AsyncSession, limit: int = 6) -> dict:
    # 1. Verifica se a impressora existe
    printer = await session.scalar(select(Impressora).where(Impressora.id == printer_id))
    if not printer:
        raise HTTPException(status_code=404, detail="Impressora não encontrada")

    # 2. Busca info de manutenção
    info_manutencao = await session.scalar(
        select(Info_Manutencao_Impressora).where(Info_Manutencao_Impressora.impressora_id == printer_id)
    )
    hoje = date.today()

    if info_manutencao:
        # 3. Se existe, verifica se ultima_atualizacao é hoje
        if info_manutencao.ultima_atualizacao != hoje:
            # Atualiza os dados
            info_dict = await get_printer_maintenance_info(printer_id, session, limit)
            info_manutencao.ultima_atualizacao = hoje
            info_manutencao.proxima_recarga = info_dict["next_recharge"]
            info_manutencao.percentual_recarga = info_dict["percentage"]
            info_manutencao.proxima_limpeza = info_dict["trash_cleaning_next_time"]
            info_manutencao.percentual_limpeza = info_dict["trash_cleaning_percentage"]
            await session.commit()
        # Retorna o registro atualizado
        return {
            "id": printer_id,
            "next_recharge": info_manutencao.proxima_recarga.strftime("%d/%m/%Y")
            if info_manutencao.proxima_recarga
            else "N/A",
            "percentage": info_manutencao.percentual_recarga,
            "trash_cleaning_next_time": info_manutencao.proxima_limpeza.strftime("%d/%m/%Y")
            if info_manutencao.proxima_limpeza
            else "N/A",
            "trash_cleaning_percentage": f"{info_manutencao.percentual_limpeza:.2f}%",
        }
    else:
        # 4. Se não existe, cria o registro
        info_dict = get_printer_maintenance_info(printer_id, session, limit)
        novo_info = Info_Manutencao_Impressora(
            impressora_id=printer_id,
            ultima_atualizacao=hoje,
            proxima_recarga=info_dict["next_recharge"],
            percentual_recarga=info_dict["percentage"],
            proxima_limpeza=info_dict["trash_cleaning_next_time"],
            percentual_limpeza=info_dict["trash_cleaning_percentage"],
        )
        await session.add(novo_info)
        await session.commit()
        return {
            "id": printer_id,
            "next_recharge": novo_info.proxima_recarga.strftime("%d/%m/%Y") if novo_info.proxima_recarga else "N/A",
            "percentage": novo_info.percentual_recarga,
            "trash_cleaning_next_time": novo_info.proxima_limpeza.strftime("%d/%m/%Y")
            if novo_info.proxima_limpeza
            else "N/A",
            "trash_cleaning_percentage": f"{novo_info.percentual_limpeza:.2f}%",
        }
