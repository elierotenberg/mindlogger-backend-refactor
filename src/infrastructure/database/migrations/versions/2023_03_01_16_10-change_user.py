"""change user

Revision ID: 3233777bab05
Revises: 3fb3cd7bd906
Create Date: 2023-03-01 16:10:51.848433

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3233777bab05"
down_revision = "3fb3cd7bd906"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("activities", "guid")
    op.drop_column("activity_histories", "guid")
    op.add_column(
        "invitations",
        sa.Column(
            "meta", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    op.drop_column("invitations", "title")
    op.drop_column("invitations", "body")
    op.add_column(
        "user_applet_accesses",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.add_column(
        "user_applet_accesses",
        sa.Column("invitor_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.add_column(
        "user_applet_accesses",
        sa.Column(
            "meta", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    op.create_foreign_key(
        op.f("fk_user_applet_accesses_invitor_id_users"),
        "user_applet_accesses",
        "users",
        ["invitor_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        op.f("fk_user_applet_accesses_owner_id_users"),
        "user_applet_accesses",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=50), nullable=True)
    )
    op.add_column(
        "users", sa.Column("last_name", sa.String(length=50), nullable=True)
    )
    op.drop_column("users", "full_name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "full_name",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
    op.drop_constraint(
        op.f("fk_user_applet_accesses_owner_id_users"),
        "user_applet_accesses",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_user_applet_accesses_invitor_id_users"),
        "user_applet_accesses",
        type_="foreignkey",
    )
    op.drop_column("user_applet_accesses", "meta")
    op.drop_column("user_applet_accesses", "invitor_id")
    op.drop_column("user_applet_accesses", "owner_id")
    op.add_column(
        "invitations",
        sa.Column("body", sa.TEXT(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "invitations",
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("invitations", "meta")
    op.add_column(
        "activity_histories",
        sa.Column(
            "guid", postgresql.UUID(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "activities",
        sa.Column(
            "guid", postgresql.UUID(), autoincrement=False, nullable=True
        ),
    )
    # ### end Alembic commands ###
