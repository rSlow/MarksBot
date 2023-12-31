"""empty message

Revision ID: 8fd90f918610
Revises: df30b04b5616
Create Date: 2023-11-26 20:21:31.881896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fd90f918610'
down_revision: Union[str, None] = 'df30b04b5616'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('marks', 'fio_index')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('marks', sa.Column('fio_index', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
