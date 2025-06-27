"""type ServiceSchema(Enum) add in field service

Revision ID: 96c6fc2cb124
Revises: 044db25453eb
Create Date: 2025-06-27 09:12:41.869812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '96c6fc2cb124'
down_revision: Union[str, Sequence[str], None] = '044db25453eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define o tipo ENUM com os valores corretos (minúsculos)
service_schema_enum = postgresql.ENUM('redis', 'postgres', 'other', name='serviceschema')


def upgrade() -> None:
    """Upgrade schema."""
    service_schema_enum.create(op.get_bind(), checkfirst=True)
    op.alter_column('system_log', 'service',
               existing_type=sa.VARCHAR(),
               type_=service_schema_enum,
               existing_nullable=False,
               postgresql_using='service::text::serviceschema')
    op.alter_column('user_log', 'service',
               existing_type=sa.VARCHAR(),
               type_=service_schema_enum,
               existing_nullable=False,
               postgresql_using='service::text::serviceschema')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('user_log', 'service',
               existing_type=service_schema_enum,
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.alter_column('system_log', 'service',
               existing_type=service_schema_enum,
               type_=sa.VARCHAR(),
               existing_nullable=False)
    service_schema_enum.drop(op.get_bind(), checkfirst=True)
