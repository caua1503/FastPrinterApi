"""unique printer_id in printer_maintenance_info

Revision ID: 2c2c2b916558
Revises: 6de5ac8a3616
Create Date: 2026-10-23 17:04:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2c2c2b916558"
down_revision: Union[str, None] = "6de5ac8a3616"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove duplicate rows, keeping the one with the highest id per printer_id
    op.execute(
        """
        DELETE FROM printer_maintenance_info a
        USING printer_maintenance_info b
        WHERE a.printer_id = b.printer_id AND a.id < b.id
        """
    )
    op.create_unique_constraint(
        "uq_printer_maintenance_info_printer_id",
        "printer_maintenance_info",
        ["printer_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_printer_maintenance_info_printer_id",
        "printer_maintenance_info",
        type_="unique",
    )
