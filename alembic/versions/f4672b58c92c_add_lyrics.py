"""add_lyrics

Revision ID: f4672b58c92c
Revises: 22822fd1f521
Create Date: 2022-06-16 12:15:09.328310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4672b58c92c'
down_revision = '22822fd1f521'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('lyrics', sa.VARCHAR(length=4000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('song', 'lyrics')
    # ### end Alembic commands ###
