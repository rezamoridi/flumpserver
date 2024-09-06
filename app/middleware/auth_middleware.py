from fastapi import HTTPException, Header
import jwt
from dotenv import load_dotenv
import os
load_dotenv()

PASSWORD_KEY = os.getenv("PASSWORD_KEY")

def auth_middleware(x_auth_token = Header()):
    try:    
        if not x_auth_token:
            raise HTTPException(status_code=401, detail="No auth token, access denied!")
            
        
        verified_token = jwt.decode(jwt=x_auth_token, key=PASSWORD_KEY, algorithms=["HS256"])
        if not verified_token:
            raise HTTPException(status_code=401, detail="token verification faildd, auth denied")
            
        uid = verified_token.get('id')
        return {"uid": uid, "token": x_auth_token}
    
    except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Token is not valid , auth proccess faile!")