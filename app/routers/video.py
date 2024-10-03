from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, Form, Depends
from middleware.auth_middleware import auth_middleware
from db import Session, get_db
from models.video import Video
from urllib.parse import quote
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

@router.post('/upload/movie', status_code=201)
def upload_movie(video:UploadFile = File(...),
                 thumbnail: UploadFile = File(...),
                 publisher: str = Form(...),
                 title: str = Form(...),
                 category: str = Form(...),
                 hex_code: str = Form(...),
                 db: Session = Depends(get_db),
                 auth_dict = Depends(auth_middleware)):
    video_id = str(uuid.uuid4())

    song_res = s3.upload_fileobj(video.file, LIARA_BUCKET_NAME, f'video/{video_id}.mp4')
    thumbnail_res = s3.upload_fileobj(thumbnail.file, LIARA_BUCKET_NAME, f'video/{video_id}.jpg')

    video_filename_encoded = quote(f'video/{video_id}.mp4')
    thumbnail_filename_encoded = quote(f'video/{video_id}.jpg')
    video_permanent_url = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{video_filename_encoded}"
    thumbnail_permanent_url = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{thumbnail_filename_encoded}"

    new_video = Video(id= video_id,
                      video_url = video_permanent_url,
                      thumbnail_url = thumbnail_permanent_url,
                      title = title,
                      publisher = publisher,
                      category = category,
                      hex_code = hex_code)
    
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video

