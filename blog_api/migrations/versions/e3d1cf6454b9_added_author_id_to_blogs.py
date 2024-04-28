"""added author_id to blogs

Revision ID: e3d1cf6454b9
Revises: de18613060a9
Create Date: 2024-04-28 13:23:03.662476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3d1cf6454b9'
down_revision = 'de18613060a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key("author_id_fk", 'users', ['author_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.drop_constraint("author_id_fk", type_='foreignkey')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###