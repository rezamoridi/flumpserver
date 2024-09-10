from sqlalchemy import TEXT, VARCHAR, Column, String
from db import Base


class Song(Base):
    __tablename__ = 'songs'

    id = Column(String, primary_key=True)
    song_url = Column(String)
    thumbnail_url = Column(String)
    artist = Column(String)
    song_name = Column(String)
    hex_code = Column(String)