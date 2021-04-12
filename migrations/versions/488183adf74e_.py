"""empty message

Revision ID: 488183adf74e
Revises: 577da079f832
Create Date: 2021-04-12 07:02:38.265623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '488183adf74e'
down_revision = '577da079f832'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurant', sa.Column('about', sa.String(length=10), nullable=True))
    op.alter_column('restaurant', 'points',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('restaurant', 'points',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('restaurant', 'about')
    # ### end Alembic commands ###
