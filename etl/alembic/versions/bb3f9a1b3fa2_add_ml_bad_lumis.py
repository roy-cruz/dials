# noqa: INP001

"""add ml bad lumis

Revision ID: bb3f9a1b3fa2
Revises: 86e3beee4a68
Create Date: 2024-03-26 16:09:50.366283

"""

from collections.abc import Sequence

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "bb3f9a1b3fa2"
down_revision: str = "86e3beee4a68"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def fact_ml_bad_lumis() -> list:
    op.execute("""
    CREATE TABLE IF NOT EXISTS fact_ml_bad_lumis (
        model_name VARCHAR(255),
        dataset_id BIGINT,
        file_id BIGINT,
        run_number INT,
        ls_number INT,
        me_id INT,
        CONSTRAINT fact_ml_bad_lumis_pk PRIMARY KEY (model_name, dataset_id, run_number, ls_number, me_id)
    );
    """)


def upgrade(engine_name: str) -> None:
    fact_ml_bad_lumis()


def downgrade(engine_name: str) -> None:
    op.drop_table("fact_ml_bad_lumis")
