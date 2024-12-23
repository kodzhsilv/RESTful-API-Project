"""Rename car model

Revision ID: 153be5ff1015
Revises: ae4c25fec8ae
Create Date: 2024-12-21 14:40:50.034920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '153be5ff1015'
down_revision: Union[str, None] = 'ae4c25fec8ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('licensePlate', sa.String(length=255), nullable=True))
    op.add_column('cars', sa.Column('garageId', sa.Integer(), nullable=True))
    op.drop_index('ix_cars_license_plate', table_name='cars')
    op.create_index(op.f('ix_cars_licensePlate'), 'cars', ['licensePlate'], unique=True)
    op.drop_constraint('cars_ibfk_1', 'cars', type_='foreignkey')
    op.create_foreign_key(None, 'cars', 'garages', ['garageId'], ['id'])
    op.drop_column('cars', 'garages')
    op.drop_column('cars', 'license_plate')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('license_plate', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('cars', sa.Column('garages', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'cars', type_='foreignkey')
    op.create_foreign_key('cars_ibfk_1', 'cars', 'garages', ['garages'], ['id'])
    op.drop_index(op.f('ix_cars_licensePlate'), table_name='cars')
    op.create_index('ix_cars_license_plate', 'cars', ['license_plate'], unique=True)
    op.drop_column('cars', 'garageId')
    op.drop_column('cars', 'licensePlate')
    # ### end Alembic commands ###