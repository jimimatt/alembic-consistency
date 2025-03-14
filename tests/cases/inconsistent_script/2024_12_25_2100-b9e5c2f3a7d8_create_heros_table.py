"""create table heroes

Revision ID: foo
Revises: a8f4b7e2c1d6
Create Date: 2025-03-12 10:20:45.789012

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b9e5c2f3a7d8"
down_revision: str | None = "a8f4b7e2c1d6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create heroes table
    op.create_table(
        "heroes",
        sa.Column("hero_id", sa.Integer, primary_key=True),
        sa.Column("hero_name", sa.String(100), nullable=False),
        sa.Column("secret_identity", sa.String(100)),
        sa.Column("powers", sa.String(255)),
        sa.Column("first_appearance", sa.Date),
        sa.Column("is_active", sa.Boolean, default=True),
        schema="superhero_universe",
    )


def downgrade() -> None:
    # Drop the heroes table when downgrading
    op.drop_table("heroes", schema="superhero_universe")
