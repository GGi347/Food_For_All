"""empty message

Revision ID: d3a5d0a3130c
Revises: e84f26d8614e
Create Date: 2021-04-25 23:56:05.361483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3a5d0a3130c'
down_revision = 'e84f26d8614e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('donation_donationRestaurant_fkey', 'donation', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('donation_donationRestaurant_fkey', 'donation', 'restaurant', ['donationRestaurant'], ['id'])
    # ### end Alembic commands ###