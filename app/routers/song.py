from fastapi import APIRouter, UploadFile, File, Form, Depends,Query, HTTPException
from middleware.auth_middleware import auth_middleware
from db import Session, get_db, joinedload, desc, join
from typing import Optional
from schemas import schemas
from models.song import Artist, Genre, SongGenre, Song
from tools import current_time, BucketObj
import datetime


router = APIRouter()

@router.post('/create_song', response_model= schemas.CreateSong , status_code=201)
def upload_song(song: UploadFile=File(...), thumbnail: UploadFile=File(...),
                title: str=Form(...),
                duration: datetime.time=Form(...),
                released_date: datetime.date=Form(...),
                genre_ids: list[int]=Form(...),
                db: Session=Depends(get_db)):
    
    thumbnail = BucketObj(file=thumbnail.file, save_name=title, 
                        destination="/song/thumbnails")
    thumbnail.upload_image()
    thumbnail_url = thumbnail.perma_link()
    song = BucketObj(file=song.file, save_name=title, 
                        destination="/songs",
                        format_="mp3")
    song.upload_image()
    thumbnail_url = thumbnail.perma_link()            
    song_url = thumbnail.perma_link()            

    new_song = Song(title=title,
                    duration=duration,
                    released_date=released_date,
                    thumbnail_url=thumbnail_url,
                    song_url=song_url,
                    created_at = current_time())
    
    
    db.add(new_song)
    db.commit()

    added_genres = []
    for genre_id in genre_ids:
        if not db.query(Genre).filter(Genre.id == genre_id).first():
            raise HTTPException(status_code=404, detail=f"genre ids[{genre_id}] not found in Genre db")
        else:    
            new_song_genre = SongGenre(song_id=new_song.id, genre_id=genre_id)
            added_genres.append(db.query(Genre).filter(Genre.id == genre_id).first().name)
            db.add(new_song_genre)
            db.commit()

    return {"id": new_song.id,
            "title": title,
            "duration": duration,
            "released_date": released_date,
            "song_url":song_url,
            "thumbnail_url":thumbnail_url,
            "created_at": new_song.created_at,
            "genres":added_genres}
    


@router.delete('/delete_song/{song_id}', response_model=schemas.DeleteSong, status_code=200)
def delete_song(song_id: int, db: Session=Depends(get_db)):
    song_db = db.query(Song).filter(Song.id == song_id).first()
    db.delete(song_db)
    db.commit()
    return song_db


@router.get("/list/")  # Specify response model if needed
def list_songs(
    genre_id: Optional[int] = Query(None, description="Filter by genre ID"),
    filter_by_releas: Optional[bool] = Query(None, description="Sort by release date (newest first)"),
    db: Session = Depends(get_db)
):

    query = db.query(Song).join(SongGenre)

    if genre_id is not None:
        query = query.filter(SongGenre.genre_id == genre_id)


    if filter_by_releas:
        query = query.order_by(desc(Song.released_date))

    songs = query.all()
    return songs




"""

-----------------------------Artist Section-------------------------------------------

"""



@router.post("/create_artist/", response_model=schemas.CreateArtist, status_code=201)
def create_artist(name: str=Form(...),
                  artistic_name: str=Form(...),
                  bio: str=Form(...),
                  avatar: UploadFile=File(...),
                  db: Session = Depends(get_db)):
    if not db.query(Artist).filter(Artist.artistic_name == artistic_name).first():
        avatar_obj = BucketObj(file=avatar.file, save_name=name, destination="/artist/profile")
        avatar_obj.upload_image()
        avatar_url = avatar_obj.perma_link()
        new_artist = Artist(name=name, artistic_name=artistic_name ,bio=bio, avatar_url=avatar_url, created_at=current_time())
        db.add(new_artist)
        db.commit()
        return new_artist
    raise HTTPException(status_code=404, detail="Duplicated artistic name")


@router.get("/get_artists/", response_model=list[schemas.Artist], status_code=200)
def read_artists(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Artist).offset(skip).limit(limit).all()


@router.get("/artists/{artist_id}", response_model=schemas.Artist)
def read_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.put("/artists/{artist_id}", response_model=schemas.UpdateArtist, status_code=200)
def update_artist(artist_id: int, avatar:UploadFile|None=File(default=None) ,name:str|None=Form(default=None), bio:str|None=Form(default=None), db: Session = Depends(get_db)):
    db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    if name:
        print(name)
        db_artist.name = name    
    if avatar:
        obj_avatar = BucketObj(file=avatar.file, save_name=db_artist.artistic_name, destination="/artists/profile")
        obj_avatar.upload_image()
        db_artist.avatar_url = obj_avatar.perma_link()
    db_artist.modified_at = current_time()
    db.commit()
    db.refresh(db_artist)
    return db_artist


@router.delete("/artists/{artist_id}", response_model=schemas.Artist)
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    db.delete(db_artist)
    db.commit()
    return db_artist



"""-----------------------------Genre Section-------------------------------------------
"""



@router.post("/genres/", response_model=schemas.Genre, status_code=201)
def create_genre(genre: schemas.BaseGenre, db: Session = Depends(get_db)):
    if not db.query(Genre).filter(Genre.name == genre.name).first():
        new_genre = Genre(name=genre.name)
        db.add(new_genre)
        db.commit()
        db.refresh(new_genre)
        return new_genre
    raise HTTPException(status_code=409, detail="Duplicated Genre Name")



@router.get("/genres/", response_model=list[schemas.Genre])
def read_genres(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Genre).offset(skip).limit(limit).all()



@router.get("/genres/{genre_id}", response_model=schemas.Genre)
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre



@router.put("/genres/{genre_id}", response_model=schemas.Genre)
def update_genre(genre_id: int, genre: schemas.BaseGenre, db: Session = Depends(get_db)):
    db_genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    for var, value in vars(genre).items():
        setattr(db_genre, var, value) if value else None
    db.commit()
    db.refresh(db_genre)
    return db_genre



@router.delete("/genres/{genre_id}", response_model=schemas.Genre)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    db_genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    db.delete(db_genre)
    db.commit()
    return db_genre