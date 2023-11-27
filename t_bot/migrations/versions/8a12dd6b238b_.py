"""empty message

Revision ID: 8a12dd6b238b
Revises: de9259b6ac1d
Create Date: 2023-11-27 14:01:58.586767

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8a12dd6b238b'
down_revision: Union[str, None] = 'de9259b6ac1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mailings', 'course',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True,
               postgresql_using='course::integer')
    op.alter_column('marks', 'group',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('marks', 'group',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    op.alter_column('mailings', 'course',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###