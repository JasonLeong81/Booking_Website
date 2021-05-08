"""empty message

Revision ID: de3e2b9ff3ef
Revises: ad740d479195
Create Date: 2021-05-08 18:18:35.735579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de3e2b9ff3ef'
down_revision = 'ad740d479195'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shopping', sa.Column('Edited_by', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shopping', 'Edited_by')
    # ### end Alembic commands ###
