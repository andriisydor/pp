
from sqlalchemy import (
   Table,
   Column,
   Integer,
   ForeignKey,
   VARCHAR,
   Boolean,

)

from sqlalchemy import orm, create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker

# "mysql://root:A2452756b@127.0.0.1/music_player"
engine = create_engine("mysql://root:123abc!!!@127.0.0.1:3306/music_player")

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(length=200))
    password = Column(VARCHAR(length=200))
    email = Column(VARCHAR(length=200))
    playlists = relationship("Playlist", backref= "user")

    def __repr__(self):
        return f"<User {self.username}, email: {self.email}>"


playlist_song = Table('playlist_song', Base.metadata,
    Column('playlist_id', ForeignKey('playlist.id'), primary_key=True),
    Column('song_id', ForeignKey('song.id'), primary_key=True)
)


class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(length=200), nullable=False)
    singer = Column(VARCHAR(length=200))
    album = Column(VARCHAR(length=200))
    duration = Column(VARCHAR(length=200),nullable=False)

    def __repr__(self):
        return f"<Song {self.name} {self.singer} {self.album}  {self.duration}>"


class Playlist(Base):
    __tablename__ = "playlist"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(length=200))
    songs = relationship(Song, secondary= playlist_song, lazy="subquery", backref=backref("playlists", lazy=True))
    user_id = Column(Integer, ForeignKey("user.id"))
    private = Column(Boolean)

    def __repr__(self):
        return f"<Playlist {self.title}  {self.private} , User: {self.user}>"