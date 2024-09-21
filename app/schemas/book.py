from pydantic import BaseModel
from pydantic import BaseModel, HttpUrl, Field
from uuid import UUID
from datetime import date

class BookBase(BaseModel):
    title: str = Field(max_length=255)
    author: str = Field(max_length=100)
    category: str = Field(max_length=50)
    pages: int = Field(ge=1)  # Ensure pages is a positive integer
    publisher: str = Field(max_length=100)
    language: str = Field(max_length=10)
    description: str = Field(max_length=300)
    hex_code: str = Field(None, max_length=6)  # Optional hex code

class BookCreate(BookBase):
    book_url: HttpUrl  # URL must be a valid HTTP URL
    thumbnail_url: HttpUrl  # URL must be a valid HTTP URL

class Book(BookBase):
    id: UUID  # UUID for the book ID
    upload_date: date  # Date when the book was uploaded

    class Config:
        orm_mode = True  # Allows compatibility with SQLAlchemy models