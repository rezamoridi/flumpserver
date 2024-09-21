from db import Base
from sqlalchemy import TEXT, VARCHAR, Column, String


class Video(Base):
    __tablename__ = 'videos'

    id = Column(String, primary_key=True)
    video_url = Column(String)
    thumbnail_url = Column(String)
    title = Column(String)
    category= Column(String)
    publisher = Column(String)
    hex_code = Column(String)