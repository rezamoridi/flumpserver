from db import Base
from sqlalchemy import Column, String, Integer, LargeBinary

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(LargeBinary)


