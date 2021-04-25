"""empty message

Revision ID: 6dbf99f522fd
Revises: 7d09669ab559
Create Date: 2021-04-25 17:41:18.113789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dbf99f522fd'
down_revision = '7d09669ab559'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donation', sa.Column('donatedByRest', sa.Integer(), nullable=True))
    op.drop_constraint('donation_donatedBy_fkey', 'donation', type_='foreignkey')
    op.drop_constraint('donation_donatedBy_fkey1', 'donation', type_='foreignkey')
    op.drop_column('donation', 'donatedBy')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donation', sa.Column('donatedBy', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('donation_donatedBy_fkey1', 'donation', 'user', ['donatedBy'], ['id'])
    op.create_foreign_key('donation_donatedBy_fkey', 'donation', 'restaurant', ['donatedBy'], ['id'])
    op.drop_column('donation', 'donatedByRest')
    # ### end Alembic commands ###