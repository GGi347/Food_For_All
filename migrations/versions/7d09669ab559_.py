"""empty message

Revision ID: 7d09669ab559
Revises: 98f0ad322bc5
Create Date: 2021-04-24 14:39:38.653491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d09669ab559'
down_revision = '98f0ad322bc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_email'), 'admin', ['email'], unique=True)
    op.create_table('user_preference',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('cuisine', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['userID'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('restID', sa.Integer(), nullable=True),
    sa.Column('item', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['restID'], ['restaurant.id'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('menu', sa.Column('discount_in_percent', sa.Integer(), nullable=True))
    op.drop_column('menu', 'availablility')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menu', sa.Column('availablility', sa.VARCHAR(length=11), autoincrement=False, nullable=True))
    op.drop_column('menu', 'discount_in_percent')
    op.drop_table('user_order')
    op.drop_table('user_preference')
    op.drop_index(op.f('ix_admin_email'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###