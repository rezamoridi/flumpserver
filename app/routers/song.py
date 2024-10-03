from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, Form, Depends
from middleware.auth_middleware import auth_middleware
from db import Session, get_db
from schemas import schemas
from models.song import Song
from models.favorite import Favorite
from sqlalchemy.orm import joinedload
"""from botocore.exceptions import NoCredentialsError"""
from urllib.parse import quote
import uuid
import os
import boto3

"""import cloudinary
import cloudinary.uploader"""

"""# Configuration       
cloudinary.config( 
    cloud_name = "durxfw3us", 
    api_key = "841768487476957", 
    api_secret = "fjdXV1PRuCxBoASJM2m3Lk8RoKk", # Click 'View API Keys' above to copy your API secret
    secure=True
)
"""
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

@router.post('/upload', response_model= schemas.Song , status_code=201)
def upload_song(song: UploadFile = File(...), 
                thumbnail: UploadFile = File(...), 
                artist: str = Form(...), 
                song_name: str = Form(...), 
                hex_code: str = Form(...),
                db: Session = Depends(get_db),
                auth_dict = Depends(auth_middleware)):
    song_id = str(uuid.uuid4())
    """song_res = cloudinary.uploader.upload(song.file, resource_type='auto', folder=f'songs/{song_id}')
    thumbnail_res = cloudinary.uploader.upload(thumbnail.file, resource_type='image', folder=f'songs/{song_id}')"""

    song_res = s3.upload_fileobj(song.file, LIARA_BUCKET_NAME, f'song/{song_id}.mp3')
    thumbnail_res = s3.upload_fileobj(thumbnail.file, LIARA_BUCKET_NAME, f'song/{song_id}.jpg')

    song_filename_encoded = quote(f'song/{song_id}.mp3')
    thumbnail_filename_encoded = quote(f'song/{song_id}.jpg')
    song_permanent_url = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{song_filename_encoded}"
    thumbnail_permanent_url = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{thumbnail_filename_encoded}"
    
    
    
    

    new_song = Song(
        id=song_id,
        song_name=song_name,
        artist=artist,
        hex_code=hex_code,
        song_url=song_permanent_url,
        thumbnail_url =thumbnail_permanent_url
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


@router.get("/list")
def list_songs(db: Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    songs = db.query(Song).all()
    return songs

@router.post('/favorite')
def favorite_song(song: schemas.FavoriteSong, 
                  db: Session=Depends(get_db), 
                  auth_details=Depends(auth_middleware)):
    # song is already favorited by the user
    user_id = auth_details['uid']

    fav_song = db.query(Favorite).filter(Favorite.song_id == song.song_id, Favorite.user_id == user_id).first()

    if fav_song:
        db.delete(fav_song)
        db.commit()
        return {'message': False}
    else:
        new_fav = Favorite(id=str(uuid.uuid4()), song_id=song.song_id, user_id=user_id)
        db.add(new_fav)
        db.commit()
        return {'message': True}
    

@router.get('/list/favorites')
def list_fav_songs(db: Session=Depends(get_db), 
               auth_details=Depends(auth_middleware)):
    user_id = auth_details['uid']
    fav_songs = db.query(Favorite).filter(Favorite.user_id == user_id).options(
        joinedload(Favorite.song),
    ).all()
    
    return fav_songs