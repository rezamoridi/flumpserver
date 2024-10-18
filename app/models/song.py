from sqlalchemy import ForeignKey, Integer, VARCHAR, Column, Date, TIME, TIMESTAMP, Boolean
from db import Base, relationship


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    song_url = Column(VARCHAR)
    thumbnail_url = Column(VARCHAR)
    title = Column(VARCHAR)
    duration = Column(TIME)
    released_date = Column(Date)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    # relationships
    genre = relationship("SongGenre", back_populates="song")
    artists = relationship("SongArtist", back_populates="song")


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, autoincrement=True)
    artistic_name = Column(VARCHAR(60), unique=True)
    name = Column(VARCHAR(255), nullable=False)
    bio = Column(VARCHAR(300))
    avatar_url = Column(VARCHAR(255))
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted = Column(Boolean, default=False)
    # relationships
    songs = relationship("SongArtist", back_populates="artist")


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50))
    cover_url = Column(VARCHAR(255))
    tracks_number = Column(Integer)
    release_date = Column(Date)
    created_at = Column(TIMESTAMP)
    modified_at = Column(TIMESTAMP)
    deleted = Column(Boolean)


class SongGenre(Base):
    __tablename__ = 'song_genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey("songs.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))
    # relationships
    song = relationship("Song", back_populates="genre")
    genre = relationship("Genre", back_populates="song_genre")


class SongArtist(Base):
    __tablename__ = 'musics_artists'

    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    song_id = Column(Integer, ForeignKey("songs.id"))
    # relationships
    song = relationship("Song", back_populates="artists")
    artist = relationship("Artist", back_populates="songs")


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50))
    # relationships
    song_genre = relationship("SongGenre", back_populates="genre")