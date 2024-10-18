"""from sqlalchemy import TEXT, Column, ForeignKey, Integer
from db import Base, relationship

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey("songs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    song = relationship('Song')
    user = relationship('User', back_populates='favorites')"""