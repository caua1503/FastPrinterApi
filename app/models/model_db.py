from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from datetime import datetime

table_registry = registry()


@table_registry.mapped_as_dataclass
class Insumo:
    __tablename__ = "insumo"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    tipo_insumo: Mapped[str]
    marca: Mapped[str]

@table_registry.mapped_as_dataclass
class Status:
    __tablename__ = "status"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    status: Mapped[str]
    ultima_atualizacao: Mapped[datetime]

@table_registry.mapped_as_dataclass
class Historico_Manutencao:
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    impressora_id: Mapped[int]
    data: Mapped[str]
    tipo_evento: Mapped[str] #preventiva, limpeza, troca de peca, concerto, Troca insumo
    descricao: Mapped[str]
    ...

@table_registry.mapped_as_dataclass
class Historico_Recarga:
    __tablename__ = "historico"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    impressora_id: Mapped[int]
    data: Mapped[str]
    tipo_evento: Mapped[str] #Reabastecimento, Troca Insumo
    id_insumo: Mapped[Insumo] = mapped_column(ForeignKey("insumo.id"))
    descricao: Mapped[str]

@table_registry.mapped_as_dataclass
class Impressora:
    __tablename__ = "impressora"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    # id_status: Mapped[Status] = mapped_column(ForeignKey("status.id"))
    # id_insumo: Mapped[Insumo] = mapped_column(ForeignKey("insumo.id"))
    id_status: Mapped[str] 
    id_insumo: Mapped[str]
    name: Mapped[str]
    marca: Mapped[str]
    model: Mapped[str]
    ip: Mapped[str] = mapped_column(unique=True)
    setor: Mapped[str] 
    descricao: Mapped[str]
    previsao: Mapped[str] 
    ultima_recarga: Mapped[str]
    ultima_manutencao: Mapped[str]
    ultima_verificacao: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False,
                                                 server_default=func.now())