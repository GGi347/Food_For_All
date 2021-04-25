"""empty message

Revision ID: e84f26d8614e
Revises: db86d2eb440b
Create Date: 2021-04-25 21:34:52.185821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e84f26d8614e'
down_revision = 'db86d2eb440b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('menu_item', sa.String(length=100), nullable=False))
    op.drop_column('item', 'item')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('item', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_column('item', 'menu_item')
    # ### end Alembic commands ###
