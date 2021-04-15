"""empty message

Revision ID: 17d113c970f5
Revises: 2151ccb696db
Create Date: 2021-04-15 06:26:03.019271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17d113c970f5'
down_revision = '2151ccb696db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.Integer(), nullable=True),
    sa.Column('receiver', sa.String(length=120), nullable=False),
    sa.Column('messageType', sa.String(length=120), nullable=False),
    sa.Column('message', sa.String(length=300), nullable=False),
    sa.ForeignKeyConstraint(['sender'], ['ngo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_receiver'), 'message', ['receiver'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_message_receiver'), table_name='message')
    op.drop_table('message')
    # ### end Alembic commands ###