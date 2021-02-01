"""Update chatrooms table

Revision ID: c0ac09727d49
Revises: 1a427112f21a
Create Date: 2021-02-01 20:40:25.960757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c0ac09727d49"
down_revision = "1a427112f21a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("chatrooms", sa.Column("name", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("chatrooms", "name")
    # ### end Alembic commands ###