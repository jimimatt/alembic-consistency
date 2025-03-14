"""create table villains

Revision ID: c1d8e6f4b2a7
Revises: a8f4b7e2c1d6
Create Date: 2025-03-12 10:25:32.456789

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c1d8e6f4b2a7"
down_revision: str | None = "a8f4b7e2c1d6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create villains table with a foreign key to heroes
    op.create_table(
        "villains",
        sa.Column("villain_id", sa.Integer, primary_key=True),
        sa.Column("villain_name", sa.String(100), nullable=False),
        sa.Column(
            "nemesis_hero_id",
            sa.Integer,
            sa.ForeignKey("superhero_universe.heroes.hero_id"),
        ),
        sa.Column("evil_plan", sa.Text),
        sa.Column("threat_level", sa.Integer),
        sa.Column("is_imprisoned", sa.Boolean, default=False),
        schema="superhero_universe",
    )

    # Add an index on the nemesis_hero_id column for faster lookups
    op.create_index(
        "ix_villains_nemesis_hero_id",
        "villains",
        ["nemesis_hero_id"],
        schema="superhero_universe",
    )


def downgrade() -> None:
    # Drop the index and table when downgrading
    op.drop_index(
        "ix_villains_nemesis_hero_id",
        table_name="villains",
        schema="superhero_universe",
    )
    op.drop_table("villains", schema="superhero_universe")
