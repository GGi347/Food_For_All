"""empty message

Revision ID: bef505cb6d0b
Revises: 65dc45fbe7b7
Create Date: 2021-04-26 06:52:15.381615

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bef505cb6d0b'
down_revision = '65dc45fbe7b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('bookingFor', sa.String(length=255), nullable=True))
    op.drop_column('booking', 'bookingOn')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('bookingOn', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('booking', 'bookingFor')
    # ### end Alembic commands ###
