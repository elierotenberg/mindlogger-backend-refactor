"""empty message

Revision ID: 267dd5b56abf
Revises: 1ca4c4d3b7df
Create Date: 2024-01-05 12:13:47.888811

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "267dd5b56abf"
down_revision = "60528d410fd1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "answers",
        sa.Column(
            "target_subject_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
    )
    op.add_column(
        "answers",
        sa.Column(
            "source_subject_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
    )
    op.add_column(
        "answers", sa.Column("relation", sa.String(length=20), nullable=True)
    )
    op.create_index(
        op.f("ix_answers_source_subject_id"),
        "answers",
        ["source_subject_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_answers_target_subject_id"),
        "answers",
        ["target_subject_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_answers_target_subject_id"), table_name="answers")
    op.drop_index(op.f("ix_answers_source_subject_id"), table_name="answers")
    op.drop_column("answers", "relation")
    op.drop_column("answers", "source_subject_id")
    op.drop_column("answers", "target_subject_id")
    # ### end Alembic commands ###
