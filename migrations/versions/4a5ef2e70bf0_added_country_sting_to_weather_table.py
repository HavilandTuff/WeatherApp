"""Added country sting to Weather table

Revision ID: 4a5ef2e70bf0
Revises: 9dcdda50589c
Create Date: 2023-01-16 18:27:42.578863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a5ef2e70bf0'
down_revision = '9dcdda50589c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weather', schema=None) as batch_op:
        batch_op.add_column(sa.Column('country', sa.String(), nullable=True))
        batch_op.drop_constraint('weather_city_unique', 'weather')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weather', schema=None) as batch_op:
        batch_op.drop_column('country')

    # ### end Alembic commands ###