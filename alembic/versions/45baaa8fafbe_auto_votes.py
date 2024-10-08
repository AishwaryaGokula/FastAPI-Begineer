"""auto-votes

Revision ID: 45baaa8fafbe
Revises: 9aad96468b47
Create Date: 2024-10-08 09:06:57.320686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '45baaa8fafbe'
down_revision: Union[str, None] = '9aad96468b47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # Drop the foreign key constraint before dropping the Users table
    op.drop_constraint('post_users_fk', 'Posts', type_='foreignkey')

    # Now you can drop the Users table safely
    op.drop_table('Users')

    # Create new users table
    op.create_table('users',
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create votes table
    op.create_table('votes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['Posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'post_id')
    )

    # Modify Posts table
    op.add_column('Posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.alter_column('Posts', 'published',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('true'))

def downgrade() -> None:
    # First, drop votes table in case it references Users
    op.drop_table('votes')

    # Create the Users table back
    op.create_table('Users',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id', name='Users_pkey'),
        sa.UniqueConstraint('email', name='Users_email_key')
    )

    # Recreate the foreign key constraint
    op.create_foreign_key('post_users_fk', 'Posts', 'Users', ['owner_id'], ['id'], ondelete='CASCADE')

    # Drop created_at column and revert changes to Posts table
    op.drop_column('Posts', 'created_at')
    op.alter_column('Posts', 'published',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('true'))

