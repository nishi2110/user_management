"""Initial migration

Revision ID: f1f3bfac2b05
Revises: 25d814bc83ed
Create Date: 2024-12-17 03:49:43.648550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1f3bfac2b05'
down_revision: Union[str, None] = '25d814bc83ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'events',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('createdby', sa.String(length=100), nullable=False),
        sa.Column('startdate', sa.DateTime(timezone=True), nullable=True),
        sa.Column('enddate', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    # ### end Alembic commands ###