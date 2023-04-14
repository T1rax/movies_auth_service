"""empty message

Revision ID: d6a36748b7d5
Revises: 419871e99949
Create Date: 2023-04-14 13:39:23.708049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6a36748b7d5'
down_revision = '419871e99949'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('histories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('remote_addr', sa.String(length=500), nullable=False))
        batch_op.add_column(sa.Column('referrer', sa.String(length=500), nullable=True))
        batch_op.alter_column('useragent',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=500),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('histories', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('useragent',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('referrer')
        batch_op.drop_column('remote_addr')

    # ### end Alembic commands ###
