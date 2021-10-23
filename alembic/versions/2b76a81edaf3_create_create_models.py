"""create create_models

Revision ID: 2b76a81edaf3
Revises: 
Create Date: 2021-10-23 15:05:17.954298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b76a81edaf3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
                     sa.Column('id', sa.Integer()),
                     sa.Column('username',sa.VARCHAR()),
                     sa.Column('password', sa.VARCHAR()),
                     sa.Column('email', sa.VARCHAR()),
                     sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('song',
                    sa.Column('id', sa.Integer()),
                    sa.Column('name', sa.VARCHAR(), nullable=False),
                    sa.Column('singer', sa.VARCHAR()),
                    sa.Column('album', sa.VARCHAR()),
                    sa.Column('duration', sa.VARCHAR(),nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('playlist',
                    sa.Column('id', sa.Integer()),
                    sa.Column('title', sa.VARCHAR()),
                    sa.Column('user_id', sa.Integer()),
                    sa.Column('private', sa.Boolean()),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'],),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('playlist_song',
                    sa.Column('playlist_id', sa.Integer()),
                    sa.Column('song_id', sa.Integer()),
                    sa.ForeignKeyConstraint(['playlist_id'], ['playlist.id'], ),
                    sa.ForeignKeyConstraint(['song_id'], ['song.id'], )
                    )


def downgrade():
    op.drop_table('user'),
    op.drop_table('song'),
    op.drop_table('playlist'),
    op.drop_table('playlist_song')

