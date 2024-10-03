from pydantic import BaseModel, Field



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


class BaseSong(BaseModel):
    song_name: str
    artist: str
    hex_code: str

class Song(BaseSong):
    song_url: str = Field(description="Url")
    thumbnail_url: str = Field(description="Url")


class FavoriteSong(BaseModel):
    song_id: str

