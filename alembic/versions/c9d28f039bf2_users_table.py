"""Users Table

Revision ID: c9d28f039bf2
Revises: 5b83318c9fb8
Create Date: 2024-10-08 08:10:09.514895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9d28f039bf2'
down_revision: Union[str, None] = '5b83318c9fb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Users',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('email',sa.String(),nullable=False,unique=True),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
                   


def downgrade() -> None:
    op.drop_table('Users')
    pass
