"""content column - Posts Table

Revision ID: 5b83318c9fb8
Revises: a06797946d09
Create Date: 2024-10-08 08:03:56.262350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b83318c9fb8'
down_revision: Union[str, None] = 'a06797946d09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('Posts','content')
    pass
