"""added roles

Revision ID: ecc54d43697d
Revises: 9f228b6d4954
Create Date: 2024-04-01 04:37:07.698823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecc54d43697d'
down_revision: Union[str, None] = '9f228b6d4954'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
