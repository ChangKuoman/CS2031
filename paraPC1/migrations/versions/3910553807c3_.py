"""empty message

Revision ID: 3910553807c3
Revises: a73094e2c7f9
Create Date: 2022-04-27 22:25:20.521820

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3910553807c3'
down_revision = 'a73094e2c7f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('fecha', sa.Date(), nullable=True))
    op.execute(f'UPDATE usuario SET fecha = CURRENT_DATE WHERE fecha IS NULL')
    op.alter_column('usuario', 'fecha', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'fecha')
    # ### end Alembic commands ###
