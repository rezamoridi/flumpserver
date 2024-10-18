from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary, Integer
from db import Base, relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

    """favorites = relationship('Favorite', back_populates='user')"""