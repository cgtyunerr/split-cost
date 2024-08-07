"""create user_group table

Revision ID: 7903432138c5
Revises: b851a32979ad
Create Date: 2024-08-07 17:18:56.869692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7903432138c5'
down_revision: Union[str, None] = 'b851a32979ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_group',
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('group_id', sa.BIGINT(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'group_id'),
    schema='group'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_group', schema='group')
    # ### end Alembic commands ###
