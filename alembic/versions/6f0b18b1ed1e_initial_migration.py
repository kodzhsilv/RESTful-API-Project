"""Initial migration

Revision ID: 6f0b18b1ed1e
Revises: 
Create Date: 2024-12-23 18:31:12.937348
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import JSON

# revision identifiers, used by Alembic.
revision = '6f0b18b1ed1e'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create 'cars' table
    op.create_table(
        'cars',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('make', sa.String(length=255), nullable=True),
        sa.Column('model', sa.String(length=255), nullable=True),
        sa.Column('productionYear', sa.Integer(), nullable=True),
        sa.Column('licensePlate', sa.String(length=255), nullable=True),
        sa.Column('garageIds', JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('licensePlate'),
    )

    # Create 'garages' table
    op.create_table(
        'garages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('city', sa.String(length=255), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create 'maintenances' table
    op.create_table(
        'maintenances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('carId', sa.Integer(), nullable=True),
        sa.Column('garageId', sa.Integer(), nullable=True),
        sa.Column('serviceType', sa.String(length=255), nullable=True),
        sa.Column('scheduledDate', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['carId'], ['cars.id'], name='fk_car_id_maintenance'),
        sa.ForeignKeyConstraint(['garageId'], ['garages.id'], name='fk_garage_id_maintenance'),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create 'car_garage' many-to-many association table
    op.create_table(
        'car_garage',
        sa.Column('car_id', sa.Integer(), nullable=False),
        sa.Column('garage_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ondelete='CASCADE', name='car_garage_ibfk_1'),
        sa.ForeignKeyConstraint(['garage_id'], ['garages.id'], ondelete='CASCADE', name='car_garage_ibfk_2'),
        sa.PrimaryKeyConstraint('car_id', 'garage_id'),
    )


def downgrade() -> None:
    op.drop_table('car_garage')
    op.drop_table('maintenances')
    op.drop_table('garages')
    op.drop_table('cars')
