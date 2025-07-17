"""add uppercase enum values

Revision ID: a3240e55af10
Revises: 156d966d521e
Create Date: 2025-07-11 13:23:22.625850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3240e55af10'
down_revision: Union[str, Sequence[str], None] = '156d966d521e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Adiciona valores MAIÚSCULOS aos ENUMs existentes. Caso já existam, ignora.
    enum_updates = {
        "serviceschema": [
            "REDIS",
            "POSTGRES",
            "OTHER",
        ],
        "loglevelschema": [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ],
        "apikeyactionschema": [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "HEAD",
            "OPTIONS",
            "TRACE",
            "CONNECT",
            "ANY",
        ],
    }

    # Adiciona os novos valores
    for enum_name, values in enum_updates.items():
        for val in values:
            op.execute(f"ALTER TYPE {enum_name} ADD VALUE IF NOT EXISTS '{val}';")

    # Converte dados existentes para maiúsculo
    op.execute("UPDATE system_log SET service = UPPER(service::text)::serviceschema, level = UPPER(level::text)::loglevelschema;")
    op.execute("UPDATE user_log SET service = UPPER(service::text)::serviceschema, level = UPPER(level::text)::loglevelschema;")
    op.execute("UPDATE api_key_log SET action = UPPER(action::text)::apikeyactionschema;")


def downgrade() -> None:
    """Downgrade schema."""
    # Não é possível remover valores de um ENUM nativamente sem recriar o tipo.
    # Portanto, o downgrade não altera os tipos nem reverte os dados.
    pass
