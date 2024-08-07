"""create group schema

Revision ID: 69f7f54aa368
Revises: 6cb7d0e083c5
Create Date: 2024-08-07 16:33:24.307491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69f7f54aa368'
down_revision: Union[str, None] = '6cb7d0e083c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS "group"')


def downgrade() -> None:
    op.execute('DROP SCHEMA IF EXISTS "group" CASCADE')
