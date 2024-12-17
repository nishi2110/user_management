"""update last login column

Revision ID: [hash]
Revises: [previous_hash]
Create Date: 2024-03-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '[hash]'
down_revision = '[previous_hash]'
branch_labels = None
depends_on = None

def upgrade():
    # Rename the column to match the new property name
    op.alter_column('users', 'last_login_at', new_column_name='_last_login_at')

def downgrade():
    # Revert the column name change
    op.alter_column('users', '_last_login_at', new_column_name='last_login_at') 