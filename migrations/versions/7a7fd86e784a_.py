"""empty message

Revision ID: 7a7fd86e784a
Revises: 6dbf99f522fd
Create Date: 2021-04-25 18:44:53.079112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a7fd86e784a'
down_revision = '6dbf99f522fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donation', sa.Column('donatedByUser', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'donation', 'user', ['donatedByUser'], ['id'])
    op.create_foreign_key(None, 'donation', 'restaurant', ['donatedByRest'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'donation', type_='foreignkey')
    op.drop_constraint(None, 'donation', type_='foreignkey')
    op.drop_column('donation', 'donatedByUser')
    # ### end Alembic commands ###