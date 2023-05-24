"""allow_edit field for activity item

Revision ID: 0c48e3afead1
Revises: 00a67bc1b11d
Create Date: 2023-05-24 02:01:34.255411

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0c48e3afead1"
down_revision = "00a67bc1b11d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "activity_item_histories",
        sa.Column("allow_edit", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "activity_items", sa.Column("allow_edit", sa.Boolean(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("activity_items", "allow_edit")
    op.drop_column("activity_item_histories", "allow_edit")
    # ### end Alembic commands ###
