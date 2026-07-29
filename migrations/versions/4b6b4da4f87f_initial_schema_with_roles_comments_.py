"""Initial schema with roles comments likes tags

Revision ID: 4b6b4da4f87f
Revises:
Create Date: 2026-07-29 14:41:42.004954

"""
from alembic import op
import sqlalchemy as sa


revision = '4b6b4da4f87f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if 'category' not in existing_tables:
        op.create_table(
            'category',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=50), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name'),
        )

    if 'tag' not in existing_tables:
        op.create_table(
            'tag',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=30), nullable=False),
            sa.PrimaryKeyConstraint('id'),
        )
        with op.batch_alter_table('tag', schema=None) as batch_op:
            batch_op.create_index('ix_tag_name', ['name'], unique=True)

    if 'comment' not in existing_tables:
        op.create_table(
            'comment',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('date_posted', sa.DateTime(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('post_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['post_id'], ['post.id']),
            sa.ForeignKeyConstraint(['user_id'], ['user.id']),
            sa.PrimaryKeyConstraint('id'),
        )

    if 'like' not in existing_tables:
        op.create_table(
            'like',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('post_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['post_id'], ['post.id']),
            sa.ForeignKeyConstraint(['user_id'], ['user.id']),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),
        )

    if 'post_tags' not in existing_tables:
        op.create_table(
            'post_tags',
            sa.Column('post_id', sa.Integer(), nullable=False),
            sa.Column('tag_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['post_id'], ['post.id']),
            sa.ForeignKeyConstraint(['tag_id'], ['tag.id']),
            sa.PrimaryKeyConstraint('post_id', 'tag_id'),
        )

    user_columns = {column['name'] for column in inspector.get_columns('user')}
    if 'role' not in user_columns:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.add_column(
                sa.Column('role', sa.String(length=20), nullable=False, server_default='user')
            )

    post_columns = {column['name'] for column in inspector.get_columns('post')}
    if 'category_id' not in post_columns:
        with op.batch_alter_table('post', schema=None) as batch_op:
            batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                'fk_post_category_id', 'category', ['category_id'], ['id']
            )

    op.execute("UPDATE user SET role = 'admin' WHERE username = 'Admin' OR email = 'admin@gmail.com'")


def downgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint('fk_post_category_id', type_='foreignkey')
        batch_op.drop_column('category_id')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    op.drop_table('post_tags')
    op.drop_table('like')
    op.drop_table('comment')
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.drop_index('ix_tag_name')
    op.drop_table('tag')
    op.drop_table('category')
