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

    if 'user' not in existing_tables:
        op.create_table(
            'user',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(length=20), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('image_file', sa.String(length=20), nullable=False),
            sa.Column('password', sa.String(length=60), nullable=False),
            sa.Column('role', sa.String(length=20), nullable=False, server_default='user'),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email'),
            sa.UniqueConstraint('username'),
        )

    if 'post' not in existing_tables:
        op.create_table(
            'post',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=100), nullable=False),
            sa.Column('date_posted', sa.DateTime(), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('category_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['category_id'], ['category.id']),
            sa.ForeignKeyConstraint(['user_id'], ['user.id']),
            sa.PrimaryKeyConstraint('id'),
        )
    elif 'category_id' not in {c['name'] for c in inspector.get_columns('post')}:
        with op.batch_alter_table('post', schema=None) as batch_op:
            batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                'fk_post_category_id', 'category', ['category_id'], ['id']
            )

    if 'support' not in existing_tables:
        op.create_table(
            'support',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=100), nullable=False),
            sa.Column('date_posted', sa.DateTime(), nullable=False),
            sa.Column('message', sa.Text(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['user.id']),
            sa.PrimaryKeyConstraint('id'),
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

    if 'user' in existing_tables and 'role' not in {c['name'] for c in inspector.get_columns('user')}:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.add_column(
                sa.Column('role', sa.String(length=20), nullable=False, server_default='user')
            )

    if inspector.has_table('user'):
        op.execute(
            sa.text(
                'UPDATE "user" SET role = \'admin\' '
                "WHERE username = 'Admin' OR email = 'admin@gmail.com'"
            )
        )


def downgrade():
    op.drop_table('post_tags')
    op.drop_table('like')
    op.drop_table('comment')
    op.drop_table('support')
    op.drop_table('post')
    op.drop_table('user')
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.drop_index('ix_tag_name')
    op.drop_table('tag')
    op.drop_table('category')
