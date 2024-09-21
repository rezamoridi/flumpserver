from db import Base
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Book(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True)
    book_url = Column(String(255), unique=True, nullable=False)
    thumbnail_url = Column(String(255), nullable=False) 
    title = Column(String(255), nullable=False)  
    author = Column(String(50), nullable=False)  
    category = Column(String(50), nullable=False)  
    pages = Column(Integer, nullable=False)  
    publisher = Column(String(50), nullable=False)  
    upload_date = Column(Date, nullable=False)  
    language = Column(String(3), nullable=False)
    description = Column(String(300))
    hex_code = Column(String(6), nullable=True)  