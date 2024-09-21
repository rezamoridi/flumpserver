from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from middleware.auth_middleware import auth_middleware
from db import Session, get_db
from models.book import Book
from schemas import book as BookSchemas
from urllib.parse import quote
from datetime import datetime
import uuid
import os
import boto3



load_dotenv()

LIARA_ENDPOINT = os.getenv("LIARA_ENDPOINT")
LIARA_ACCESS_KEY = os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY = os.getenv("LIARA_SECRET_KEY")
LIARA_BUCKET_NAME = os.getenv("LIARA_BUCKET_NAME")


s3 = boto3.client(
    "s3",
    endpoint_url=LIARA_ENDPOINT,
    aws_access_key_id=LIARA_ACCESS_KEY,
    aws_secret_access_key=LIARA_SECRET_KEY,
)

router = APIRouter()

@router.post("/upload/book", response_model=BookSchemas.Book, status_code=201)
def upload_book(
    bookbase: BookSchemas.BookBase = Depends(),  # Use Depends to extract the BookBase
    book: UploadFile = File(...),  # Use File(...) for file uploads
    thumbnail: UploadFile = File(...),  # Use File(...) for file uploads
    auth_dict = Depends(auth_middleware),
    db: Session = Depends(get_db),
):
    # Your existing logic here...
    book_id = str(uuid.uuid4())

    # Upload the book file and thumbnail to S3
    try:
        s3.upload_fileobj(book.file, LIARA_BUCKET_NAME, f'book/{book_id}.pdf')
        s3.upload_fileobj(thumbnail.file, LIARA_BUCKET_NAME, f'book/{book_id}.jpg')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")

    # Generate permanent URLs for the uploaded files
    book_filename_encoded = quote(f'book/{book_id}.pdf')
    thumbnail_filename_encoded = quote(f'book/{book_id}.jpg')
    book_permanent_url = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{book_filename_encoded}"
    thumbnail_permanent_url = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{thumbnail_filename_encoded}"

    # Create a new book instance
    new_book = Book(
        id=book_id,
        book_url=book_permanent_url,
        thumbnail_url=thumbnail_permanent_url,
        title=bookbase.title,
        pages=bookbase.pages,
        author=bookbase.author,
        publisher=bookbase.publisher,
        category=bookbase.category,
        language=bookbase.language,
        description=bookbase.description,
        upload_date=datetime.now(),
        hex_code=bookbase.hex_code
    )

    # Save the new book to the database
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/list/book/recent")
def recent_added(db: Session = Depends(get_db)):
    recent_books = db.query(Book).order_by(Book.upload_date).limit(3)

    return recent_books

@router.get("/list/book/")
def recent_added(db: Session = Depends(get_db)):
    books = db.query(Book).all()

    return books