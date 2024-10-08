"""Foreign Key Changes

Revision ID: 213f80ebea95
Revises: d266aeb33a49
Create Date: 2024-10-08 08:40:12.621920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '213f80ebea95'
down_revision: Union[str, None] = 'd266aeb33a49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

    


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name='Posts')
    op.drop_column('Posts','owner_id')
    pass
