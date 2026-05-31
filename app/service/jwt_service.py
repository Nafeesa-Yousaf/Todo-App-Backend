from decouple import config
import jwt
import time
from fastapi import HTTPException,status
from app.repository.auth_repo import AuthRepository
from app.service.hash_service import HashService

JWT_SECRET=config("JWT_SECRET")
JWT_ALGORITHM=config("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE=900 #15 minutes
REFRESH_TOKEN_EXPIRES=864000 #10 days

class JwtService:
    @staticmethod
    def create_access_token(user_id:int)->str:
        payload={
            'user_id':user_id,
            'expires':time.time() +ACCESS_TOKEN_EXPIRE
        }
        token= jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
        return token
    
    @staticmethod
    def create_refresh_token(user_id:int,user_email:str)->str:
        payload={
            'user_id':user_id,
            'user_email':user_email,
            'expires':time.time() +REFRESH_TOKEN_EXPIRES
        }
        token= jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def decode_jwt(jwt_token:str)->dict:
        try:
            decoded_token= jwt.decode(jwt_token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
            if decoded_token["expires"]>=time.time():
                return decoded_token  
            else:
                HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" Access Token Expired")
        except:
            print("unable to decode token")
            return None
        
    @staticmethod
    def verify_refresh_token(refresh_token:str)->int:
        decoded_token=jwt.decode(refresh_token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"]<=time.time():
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "Refresh Token Expired")
        user_token=AuthRepository().get_refresh_token(decoded_token["user_id"])
        hash_token=HashService.hash_string(refresh_token)
        if(user_token==hash_token):
            return decoded_token["user_id"]
        else:
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Refresh Token")
        
