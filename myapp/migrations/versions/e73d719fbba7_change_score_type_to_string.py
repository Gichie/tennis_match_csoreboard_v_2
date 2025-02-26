"""Change Score type to String

Revision ID: e73d719fbba7
Revises: d2eea0986132
Create Date: 2025-02-24 09:06:25.911742

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e73d719fbba7"
down_revision: Union[str, None] = "d2eea0986132"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "matches",
        sa.Column("current_game_state", sa.String(length=26), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("matches", "current_game_state")
    # ### end Alembic commands ###
