"""empty message

Revision ID: 025786338726
Revises: 8a12dd6b238b
Create Date: 2023-11-27 15:35:13.932256

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '025786338726'
down_revision: Union[str, None] = '8a12dd6b238b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mailings', 'all',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mailings', 'all',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###