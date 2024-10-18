from pydantic import BaseModel, Field
from typing import Optional
from fastapi import UploadFile, Form, File
import datetime


class UserLogin(BaseModel):
    email: str
    password: str




class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class User(UserCreate):
    id : str


class RespLogin(BaseModel):
    token:str
    user: User



""" --------------------------------------- Song Section ------------------------------------------"""


class BaseSong(BaseModel):
    title: str
    duration: datetime.time
    released_date: datetime.date
    genres: list[str]

class CreateSong(BaseSong):
    id: int
    song_url: str
    thumbnail_url: str
    created_at: datetime.datetime



class UpdateSong(CreateSong):
    modified_at: Optional[datetime.datetime] = None


class DeleteSong(UpdateSong):
    deleted_at: Optional[datetime.datetime] = None


class Song(DeleteSong):
    pass




""" --------------------------------------- Artist Section ------------------------------------------"""




class BaseArtist(BaseModel):
    artistic_name: str
    name: str
    bio: str

class CreateArtist(BaseArtist):
    id: int
    avatar_url: str
    created_at: datetime.datetime

class UpdateArtist(CreateArtist):
    modified_at: Optional[datetime.datetime] = None

class Artist(UpdateArtist):
    deleted_at: Optional[datetime.datetime] = None


""" --------------------------------------- Genre Section ------------------------------------------"""



class BaseGenre(BaseModel):
    name: str

class Genre(BaseGenre):
    id: int


