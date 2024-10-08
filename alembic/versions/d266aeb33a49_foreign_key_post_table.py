"""Foreign Key - Post table

Revision ID: d266aeb33a49
Revises: c9d28f039bf2
Create Date: 2024-10-08 08:32:09.076871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd266aeb33a49'
down_revision: Union[str, None] = 'c9d28f039bf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="Posts",referent_table="Users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk')
    pass
