"""add analytics table

Revision ID: [auto-generated hash]
Revises: [previous revision hash]
Create Date: [timestamp]

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '[auto-generated hash]'
down_revision = '[previous revision hash]'
branch_labels = None
depends_on = None

def upgrade():
    # Create UserRole enum type if it doesn't exist
    userrole = postgresql.ENUM('ANONYMOUS', 'AUTHENTICATED', 'MANAGER', 'ADMIN', name='userrole')
    userrole.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'user_analytics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('session_id', sa.String(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('previous_role', sa.Enum('ANONYMOUS', 'AUTHENTICATED', 'MANAGER', 'ADMIN', name='userrole'), nullable=True),
        sa.Column('new_role', sa.Enum('ANONYMOUS', 'AUTHENTICATED', 'MANAGER', 'ADMIN', name='userrole'), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('event_metadata', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('user_analytics') 