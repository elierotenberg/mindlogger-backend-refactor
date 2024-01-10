"""Add user_id column to invitations

Revision ID: 3fb536a58c94
Revises: 5130eba9f698
Create Date: 2023-12-26 14:51:42.568199

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3fb536a58c94"
down_revision = "5130eba9f698"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "invitations",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        op.f("fk_invitations_user_id_users"),
        "invitations",
        "users",
        ["user_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_invitations_user_id_users"), "invitations", type_="foreignkey"
    )
    op.drop_column("invitations", "user_id")
    # ### end Alembic commands ###
