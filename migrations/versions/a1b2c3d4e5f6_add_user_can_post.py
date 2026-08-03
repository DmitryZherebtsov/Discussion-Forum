"""Add can_post approval flag to users

Revision ID: a1b2c3d4e5f6
Revises: 4b6b4da4f87f
Create Date: 2026-08-03 17:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f6'
down_revision = '4b6b4da4f87f'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {c['name'] for c in inspector.get_columns('user')}

    if 'can_post' not in columns:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.add_column(
                sa.Column('can_post', sa.Boolean(), nullable=False, server_default=sa.false())
            )

    op.execute(sa.text('UPDATE "user" SET can_post = true WHERE role = \'admin\''))


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('can_post')
