"""Add timezone offset to answers

Revision ID: 23fe6ccfb031
Revises: 736adb0ea547
Create Date: 2024-03-18 17:14:58.183938

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "23fe6ccfb031"
down_revision = "736adb0ea547"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "answers_items",
        sa.Column(
            "tz_offset",
            sa.Integer(),
            nullable=True,
            comment="Local timezone offset in minutes",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("answers_items", "tz_offset")
    # ### end Alembic commands ###
