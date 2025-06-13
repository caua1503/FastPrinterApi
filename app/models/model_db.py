from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from datetime import datetime, date
from typing import Optional

table_registry = registry()

@table_registry.mapped_as_dataclass
class Tipo_Insumo:
    __tablename__ = "tipo_insumo"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]

@table_registry.mapped_as_dataclass
class Insumo:
    __tablename__ = "insumo"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    tipo_insumo: Mapped[int] = mapped_column(ForeignKey("tipo_insumo.id"))
    marca: Mapped[str]
    descricao: Mapped[Optional[str]]

@table_registry.mapped_as_dataclass
class Status:
    __tablename__ = "status"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    status: Mapped[str]
    descricao: Mapped[Optional[str]]

@table_registry.mapped_as_dataclass
class Historico_Status:
    __tablename__ = "historico_status"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    impressora_id: Mapped[int] = mapped_column(ForeignKey("impressora.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    data: Mapped[date]
    descricao: Mapped[Optional[str]]

@table_registry.mapped_as_dataclass
class Historico_Manutencao:
    __tablename__ = "historico_manutencao"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    impressora_id: Mapped[int]
    data: Mapped[date]
    tipo_evento: Mapped[str] #preventiva, limpeza, troca de peca, concerto, Troca insumo
    descricao: Mapped[Optional[str]]
    ...

@table_registry.mapped_as_dataclass
class Historico_Recarga:
    __tablename__ = "historico"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    impressora_id: Mapped[int]
    data: Mapped[date]
    tipo_evento: Mapped[str] #Reabastecimento, Troca Insumo
    id_insumo: Mapped[Insumo] = mapped_column(ForeignKey("insumo.id"))
    descricao: Mapped[Optional[str]]

@table_registry.mapped_as_dataclass
class Impressora:
    __tablename__ = "impressora"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_status: Mapped[int] = mapped_column(ForeignKey("status.id"))
    id_insumo: Mapped[int] = mapped_column(ForeignKey("insumo.id"))
    name: Mapped[str]
    marca: Mapped[str]
    model: Mapped[str]
    ip: Mapped[str] = mapped_column(unique=True)
    setor: Mapped[str] 
    descricao: Mapped[Optional[str]]
    previsao: Mapped[Optional[date]] 
    ultima_recarga: Mapped[Optional[date]]
    ultima_manutencao: Mapped[Optional[date]]
    ultima_verificacao: Mapped[Optional[date]]
    created_at: Mapped[datetime] = mapped_column(init=False,
                                                 server_default=func.now())