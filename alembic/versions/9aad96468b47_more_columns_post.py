"""More Columns - Post

Revision ID: 9aad96468b47
Revises: 213f80ebea95
Create Date: 2024-10-08 08:51:26.562537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9aad96468b47'
down_revision: Union[str, None] = '213f80ebea95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE',default=True))


def downgrade() -> None:
    op.drop_column('Posts','published')
