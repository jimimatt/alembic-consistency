"""create schema superhero

Revision ID: a8f4b7e2c1d6
Revises: b9e5c2f3a7d8
Create Date: 2025-03-12 10:15:22.123456

"""

from collections.abc import Sequence

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a8f4b7e2c1d6"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create the schema for our superhero database
    op.execute("CREATE SCHEMA IF NOT EXISTS superhero_universe;")


def downgrade() -> None:
    # Drop the schema when downgrading
    op.execute("DROP SCHEMA IF EXISTS superhero_universe CASCADE;")
