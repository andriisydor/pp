import os
import sys
sys.path.append("/home/yuliamarkiv/pp")

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


DB_URI = os.getenv('DB_URI','postgresql://tecmint:rolny34F@localhost:5432/test')


engine = create_engine(DB_URI)
SessionFactory = sessionmaker(bind= engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR)
    password = Column(VARCHAR)
    email = Column(VARCHAR)
    playlists = relationship("Playlist", backref= "user")


    def __repr__(self):
        return f"<User {self.username}, email: {self.email}>"

playlist_song = Table('playlist_song', Base.metadata,
    Column('playlist_id', ForeignKey('playlist.id'), primary_key=True),
    Column('song_id', ForeignKey('song.id'), primary_key=True)
)
class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    singer = Column(VARCHAR)
    album = Column(VARCHAR)
    duration = Column(VARCHAR,nullable=False)

    def __repr__(self):
        return f"<Song {self.name} {self.singer} {self.album}  {self.duration}>"


class Playlist(Base):
    __tablename__ = "playlist"
    id = Column(Integer,primary_key=True)
    title = Column(VARCHAR)
    songs = relationship(Song, secondary= playlist_song, lazy="subquery", backref=backref("playlists", lazy=True))
    user_id = Column(Integer, ForeignKey("user.id"))
    private = Column(Boolean)
    def __repr__(self):
        return f"<Playlist {self.title}  {self.private} , User: {self.user}>"



