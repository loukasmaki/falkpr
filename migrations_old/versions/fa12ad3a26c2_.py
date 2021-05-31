"""empty message

Revision ID: fa12ad3a26c2
Revises: 
Create Date: 2021-05-24 19:55:29.845652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa12ad3a26c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('foton',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('namn', sa.String(length=128), nullable=True),
    sa.Column('fotograf', sa.String(length=128), nullable=True),
    sa.Column('hyll_id', sa.Integer(), nullable=True),
    sa.Column('kategori', sa.String(length=64), nullable=True),
    sa.Column('datum', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hyllor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('beskrivning', sa.String(length=128), nullable=True),
    sa.Column('lokal_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lokaler',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('namn', sa.String(length=64), nullable=True),
    sa.Column('koordinatref', sa.String(length=64), nullable=True),
    sa.Column('kommun', sa.String(length=128), nullable=True),
    sa.Column('län', sa.String(length=128), nullable=True),
    sa.Column('förälder_id', sa.Integer(), nullable=True),
    sa.Column('år_hittad', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('observationer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person', sa.String(length=64), nullable=True),
    sa.Column('såg_falk', sa.Boolean(), nullable=True),
    sa.Column('bekräftad_häckning', sa.Boolean(), nullable=True),
    sa.Column('plats', sa.String(length=64), nullable=True),
    sa.Column('datum', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_table('återfynd',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hb', sa.String(length=20), nullable=True),
    sa.Column('vb', sa.String(length=20), nullable=True),
    sa.Column('levande', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('falkar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vikt', sa.Integer(), nullable=True),
    sa.Column('kön', sa.String(length=1), nullable=True),
    sa.Column('hb', sa.String(length=20), nullable=True),
    sa.Column('vb', sa.String(length=20), nullable=True),
    sa.Column('hp10', sa.Integer(), nullable=True),
    sa.Column('hp7', sa.Integer(), nullable=True),
    sa.Column('sp', sa.Integer(), nullable=True),
    sa.Column('ålder', sa.Integer(), nullable=True),
    sa.Column('kräva', sa.String(length=10), nullable=True),
    sa.Column('foto', sa.String(length=64), nullable=True),
    sa.Column('märkare', sa.String(length=64), nullable=True),
    sa.Column('övrigt', sa.String(length=128), nullable=True),
    sa.Column('ringmärkt_datum', sa.DateTime(), nullable=True),
    sa.Column('lokal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lokal_id'], ['lokaler.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('country', sa.String(length=64), nullable=True),
    sa.Column('club', sa.String(length=64), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_table('falk_återfynd',
    sa.Column('falk_id', sa.Integer(), nullable=False),
    sa.Column('återfynd_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['falk_id'], ['falkar.id'], ),
    sa.ForeignKeyConstraint(['återfynd_id'], ['återfynd.id'], ),
    sa.PrimaryKeyConstraint('falk_id', 'återfynd_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('falk_återfynd')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('falkar')
    op.drop_table('återfynd')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    op.drop_table('observationer')
    op.drop_table('lokaler')
    op.drop_table('hyllor')
    op.drop_table('foton')
    # ### end Alembic commands ###
