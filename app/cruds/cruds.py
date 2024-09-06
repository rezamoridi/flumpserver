import jwt.exceptions
from models import users as UserModels
from schemas import schemas
from db import Session
from fastapi import HTTPException
import uuid
import bcrypt
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
PASSWORD_KEY = os.getenv("PASSWORD_KEY")





"""def Exist_user(email: str, db: Session):
    user_query = db.query(UserModels.User).filter(UserModels.User.email == email).first()

    if not user_query:
        raise HTTPException(status_code=404, detail= "User Not Found")

    return user_query"""



def Create_User(user: schemas.UserCreate, db: Session):
    Exist_user = db.query(UserModels.User).filter(UserModels.User.email == user.email).first()
    if Exist_user:
        raise HTTPException(status_code=409, detail= "Create User Failed, Duplicated User Found")
    
    hash_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    user_db = UserModels.User(id=str(uuid.uuid4()), 
                              name= user.name, 
                              email= user.email,
                              password= hash_pw
                              )
    db.add(user_db)
    db.commit()

    return user_db




def Login_user(user: schemas.UserLogin, db: Session):
    user_db = db.query(UserModels.User).filter(UserModels.User.email == user.email).first()

    check_hash_pw = bcrypt.checkpw(user.password.encode(), user_db.password)

    if not user_db or not check_hash_pw:
        raise HTTPException(status_code=404, detail=f"Login Failed, User With {user.email} and Password not found")
    
    token = jwt.encode(payload={"id": user_db.id}, key=PASSWORD_KEY)

    return {"token": token, "user": user_db}


def Get_user(user_uid: str, db: Session):
    user = db.query(UserModels.User).filter(UserModels.User.id == user_uid).first()
    if not user:
        raise HTTPException (status_code = 404, detail = "User not found")
    
    return user