"""create-user-schema

Revision ID: 577800ac1eee
Revises: 
Create Date: 2024-08-06 22:53:11.877357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '577800ac1eee'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS "user"')


def downgrade() -> None:
    op.execute('DROP SCHEMA IF EXISTS "user" CASCADE')
