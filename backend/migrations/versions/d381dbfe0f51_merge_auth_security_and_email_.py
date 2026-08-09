"""merge auth security and email verification heads

Revision ID: d381dbfe0f51
Revises: 0005_add_auth_security, 0006_add_email_verification
Create Date: 2026-08-08 13:54:36.886245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd381dbfe0f51'
down_revision: Union[str, Sequence[str], None] = ('0005_add_auth_security', '0006_add_email_verification')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
