"""empty message

Revision ID: 2ce4dd92fc99
Revises: 488183adf74e
Create Date: 2021-04-14 09:01:43.215943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ce4dd92fc99'
down_revision = '488183adf74e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('NGO',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ngoName', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('contact_number', sa.String(length=15), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('about', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_NGO_email'), 'NGO', ['email'], unique=True)
    op.create_index(op.f('ix_NGO_ngoName'), 'NGO', ['ngoName'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_NGO_ngoName'), table_name='NGO')
    op.drop_index(op.f('ix_NGO_email'), table_name='NGO')
    op.drop_table('NGO')
    # ### end Alembic commands ###
