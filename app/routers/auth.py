from dotenv import load_dotenv
from middleware.auth_middleware import auth_middleware
from db import get_db, Session
from schemas import schemas
from cruds import cruds
from fastapi import APIRouter, Depends
import os

load_dotenv()
PASSWORD_KEY = os.getenv("PASSWORD_KEY")
router = APIRouter()


@router.post('/signup', response_model=schemas.User, status_code=201)
def signup_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    return cruds.Create_User(user= user, db= db)
    

@router.post('/login', response_model=schemas.RespLogin)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return cruds.Login_user(user= user, db= db)
 

@router.get('/')
def current_user_data(user_dict = Depends(auth_middleware), db: Session=Depends(get_db)):
    return cruds.Get_user(user_uid=user_dict["uid"], db= db)