"""add_data_in_role

Revision ID: 2b23e8910097
Revises: 3b737a5ba060
Create Date: 2024-05-04 20:01:03.653472

"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b23e8910097"
down_revision: Union[str, None] = "3b737a5ba060"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    role_table = sa.table(
        "role",
        sa.Column("name", sa.String(16), nullable=False),
        sa.Column("permission", sa.JSON, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),  # Ensure to add this line
        sa.Column("updated_at", sa.DateTime, nullable=False),  # Ensure to add this line
    )

    current_time = datetime.utcnow()
    op.bulk_insert(
        role_table,
        [
            {
                "name": "Admin",
                "permission": {"admin": True},
                "created_at": current_time,
                "updated_at": current_time,
            },
            {
                "name": "User",
                "permission": {"admin": False},
                "created_at": current_time,
                "updated_at": current_time,
            },
            {
                "name": "Moderator",
                "permission": {"moderate": True},
                "created_at": current_time,
                "updated_at": current_time,
            },
            # ... дополнительные записи ...
        ],
    )


def downgrade() -> None:
    pass
