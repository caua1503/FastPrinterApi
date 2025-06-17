from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

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
class Historico_Lixeira_Impressora:
    __tablename__ = "historico_lixeira_impressora"  # historico de limpeza da lixeira
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    impressora_id: Mapped[int] = mapped_column(ForeignKey("impressora.id"))
    data: Mapped[date]
    descricao: Mapped[Optional[str]]


@table_registry.mapped_as_dataclass
class Historico_Status:  # historico de status da impressora, em manutencao, recargas, quando chegou em critico e etc
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
    tipo_evento: Mapped[str]  # preventiva, limpeza, troca de peca, concerto, Troca insumo
    descricao: Mapped[Optional[str]]


@table_registry.mapped_as_dataclass
class Historico_Recarga:
    __tablename__ = "historico"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    impressora_id: Mapped[int]
    data: Mapped[date]
    tipo_evento: Mapped[str]  # Reabastecimento, Troca Insumo
    id_insumo: Mapped[Insumo] = mapped_column(ForeignKey("insumo.id"))
    descricao: Mapped[Optional[str]]


@table_registry.mapped_as_dataclass
class Info_Manutencao_Impressora:
    __tablename__ = "info_manutencao_impressora"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    impressora_id: Mapped[int] = mapped_column(ForeignKey("impressora.id"))
    ultima_atualizacao: Mapped[date]
    proxima_recarga: Mapped[Optional[date]]
    proxima_limpeza: Mapped[Optional[date]]
    percentual_recarga: Mapped[float]
    percentual_limpeza: Mapped[float]


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
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class Historico_Alerta:
    __tablename__ = "alerta"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    impressora_id: Mapped[int] = mapped_column(ForeignKey("impressora.id"))
    data: Mapped[date]
    tipo_alerta: Mapped[str]
    descricao: Mapped[Optional[str]]


@table_registry.mapped_as_dataclass
class Usuario:
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    senha_hash: Mapped[str]
    codigo_hash: Mapped[str]
    api_key: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class Permissoes:
    __tablename__ = "permissoes"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    permissoes: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class Usuario_Configuracao:
    __tablename__ = "usuario_configuracao"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    nome_usuario: Mapped[str]
    webhook_enable: Mapped[bool] = mapped_column(default=False)
    webhook_url: Mapped[Optional[str]] = mapped_column(default=None)
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
