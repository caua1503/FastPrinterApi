"""field creation: created_at for date filters

Revision ID: 044db25453eb
Revises: d1f84665f769
Create Date: 2025-06-27 09:02:28.100264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '044db25453eb'
down_revision: Union[str, Sequence[str], None] = 'd1f84665f769'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define os tipos ENUM
log_level_old = postgresql.ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', name='loglevel')
log_level_new = postgresql.ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', name='loglevelschema')


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('system_log', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.add_column('user_log', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))

    log_level_new.create(op.get_bind(), checkfirst=True)
    op.alter_column('system_log', 'level',
               existing_type=log_level_old,
               type_=log_level_new,
               existing_nullable=False,
               postgresql_using='level::text::loglevelschema')
    op.alter_column('user_log', 'level',
               existing_type=log_level_old,
               type_=log_level_new,
               existing_nullable=False,
               postgresql_using='level::text::loglevelschema')
    log_level_old.drop(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    """Downgrade schema."""
    log_level_old.create(op.get_bind(), checkfirst=True)
    op.alter_column('user_log', 'level',
               existing_type=log_level_new,
               type_=log_level_old,
               existing_nullable=False,
               postgresql_using='level::text::loglevel')
    op.alter_column('system_log', 'level',
               existing_type=log_level_new,
               type_=log_level_old,
               existing_nullable=False,
               postgresql_using='level::text::loglevel')
    log_level_new.drop(op.get_bind(), checkfirst=True)

    op.drop_column('user_log', 'created_at')
    op.drop_column('system_log', 'created_at')
