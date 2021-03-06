"""empty message

Revision ID: fe6f5ede2623
Revises: 99c78fa559ea
Create Date: 2021-05-25 21:37:06.192102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe6f5ede2623'
down_revision = '99c78fa559ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('falkar', sa.Column('duvringar', sa.Boolean(), nullable=True))
    op.add_column('falkar', sa.Column('närvarande', sa.String(length=128), nullable=True))
    op.add_column('falkar', sa.Column('påse', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('falkar', 'påse')
    op.drop_column('falkar', 'närvarande')
    op.drop_column('falkar', 'duvringar')
    # ### end Alembic commands ###
