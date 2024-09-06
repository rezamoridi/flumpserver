from pydantic import BaseModel



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